import qad_api.core.internal.backend as backend

import yaml
import os
from typing import Optional, Union, Callable, Dict

from requests import Response
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError


class AuthMethods:
    InteractiveConsole = "console"


class Session:
    """
    The authentication layer of the QAD API.

    This class lets the user authenticate with the QAD API, stores the token
    for reuse, and serves as an HTTP middleware layer which adds the headers
    needed to pass the tokens along with any subsequent requests.
    """

    def __init__(
        self,
        auth_method: str = AuthMethods.InteractiveConsole,
    ):
        self._backend = backend

        # Set callbacks depending on the method the user chose to interact with the authorization layer
        if auth_method == AuthMethods.InteractiveConsole:
            self._authorization_callback = self._authorization_callback_console
            self._authorization_feedback = self._authorization_feedback_console
        else:
            raise Exception("Invalid method")

        # Read token from local file
        try:
            with open(self._backend.token_db_file) as file:
                self.stored_token = yaml.safe_load(file)
        except:
            self.stored_token = None

        # OAuth2 Session handler
        self._oauth = OAuth2Session(
            client_id=self._backend.client_id,
            redirect_uri=self._backend.redirect_uri,
            token=self.stored_token
        )

    def _use_token(self, token: dict):
        self.token = token
        self.id_token = token["id_token"]
        self._oauth.access_token = self.id_token

        # Store token in local file
        try:
            if not os.path.isdir(os.path.dirname(self._backend.token_db_file)):
                os.makedirs(os.path.dirname(self._backend.token_db_file))
            with open(self._backend.token_db_file, 'w') as file:
                yaml.dump(dict(token), file)
        except Exception as e:
            print("Warning: failed to store token:")
            print(e)

    def _init_post_auth(self):
        # Fetch API status and user ID
        try:
            info = self.request('get', 'info').json()
            self.userid = info['userId']
            self.api_version = info['version']
            return True
        except:
            return False

    def resume(self):
        """Try to resume a previous session without reauthentication."""
        
        # Apply stored token internally
        if not self.stored_token:
            return False
        self._use_token(self.stored_token)

        # See if token is still valid (this might refresh the access/id token but even this can fail if the refresh token expired)
        if not self._init_post_auth():
            return False

        self._authorization_feedback(True)
        return True

    def authorize(self):
        """Try to authorize, starting a new session."""

        # Make the user call the authorization URI to log in
        authorization_url, state = self._oauth.authorization_url(self._backend.authorization_base_url)
        code = self._authorization_callback(authorization_url)

        if not code:
            return False

        # Fetch the token
        token = self._oauth.fetch_token(self._backend.token_url, code, include_client_id=True)
        self._use_token(token)
        
        # See if everything worked
        if not self._init_post_auth():
            return False
            
        self._authorization_feedback(False)
        return True

    def _authorization_callback_console(self, authorization_url: str) -> str:
        print("")
        print("-------------------------------------------------------------------------------")
        print("Authorization URI:")
        print(authorization_url)
        print("-------------------------------------------------------------------------------")
        print("")
        print("To authorize, do the following:")
        print("")
        print(" 1.  Use your web browser to navigate to the authorization URI above.")
        print(" 2.  When asked for a login, use your credentials for QAD cloud.")
        print(" 3.  You'll see a webpage with a code. Paste that below and hit the return key.")
        print("")
        print("To cancel, leave the input empty and just hit the return key.")
        print("")
        return input("> ")


    def _authorization_feedback_console(self, is_resume: bool):
        print("")
        if is_resume:
            print("Successfully resumed previous session with QAD Cloud backend.")
        else:
            print("Successfully authenticated with QAD Cloud backend.")
        print("")
        print(f"Your user ID: {self.userid}")
        print("")
        
        
    def request(self, method: str, path: str, **kwargs) -> Response:
        """*Internal.* Make a request with the authentication headers.
        
        This might refresh the token, but never asks for a whole fresh authentication.
        """
        url = self._backend.api_base_url + path
        try:
            return self._oauth.request(method, url, **kwargs)
        except TokenExpiredError:
            token = self._oauth.refresh_token(self._backend.token_url, client_id=self._backend.client_id)
            self._use_token(token)
            # Repeat request
            return self._oauth.request(method, url, **kwargs)


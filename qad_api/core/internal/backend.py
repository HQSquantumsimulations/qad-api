import os
import appdirs


api_base_url = os.environ.get(
    "QAD_API_BASE_URL",
    "https://api.qad.quantumsimulations.de/v1/"
)

client_id = os.environ.get(
    "QAD_API_CLIENT_ID",
    "..."
)

authorization_base_url = os.environ.get(
    "QAD_API_AUTH_BASE_URL",
    "https://qad.auth.eu-central-1.amazoncognito.com/oauth2/authorize"
)

redirect_uri = os.environ.get(
    "QAD_API_AUTH_REDIRECT_URI",
    "https://qad.quantumsimulations.de/auth/api"
)

token_url = os.environ.get(
    "QAD_API_TOKEN_URL",
    "https://qad.auth.eu-central-1.amazoncognito.com/oauth2/token"
)

token_db_file = os.environ.get(
    "QAD_API_TOKEN_DB_FILE",
    os.path.join(appdirs.user_data_dir('qad_api', 'hqs'), 'auth', 'access_token.db')
)

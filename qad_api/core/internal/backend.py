# Copyright 2020 HQS Quantum Simulations GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import appdirs


api_base_url = os.environ.get(
    "QAD_API_BASE_URL",
    "https://api.qad.quantumsimulations.de/v1/"
)

client_id = os.environ.get(
    "QAD_API_CLIENT_ID",
    "3eq9b50srofnfusqlpvcsj5suq"
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

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

from qad_api import QAD_API

# Creating an QAD_API instance will authenticate the user with the backend
qad = QAD_API()

# Get the "credits" object of the current user, which contains more than
# just the number of credits, but also information about credits renewal.
response = qad.account.get_credits()

# Print the current number of credits
print(f"You have {response.credits} credits to do awesome stuff!")

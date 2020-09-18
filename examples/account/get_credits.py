from qad_api import QAD_API

# Creating an QAD_API instance will authenticate the user with the backend
qad = QAD_API()

# Get the "credits" object of the current user, which contains more than
# just the number of credits, but also information about credits renewal.
response = qad.account.get_credits()

# Print the current number of credits
print(f"You have {response.credits} credits to do awesome stuff!")

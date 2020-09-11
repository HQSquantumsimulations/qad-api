from qad_api import QAD_API

qad = QAD_API()

response = qad.account.get_credits()
print(response.credits)

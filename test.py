# import requests
# mobile = 917567677094
# message = 'Use OTP 1203 to login'
# response = requests.get(f'http://sms.smsindori.com/http-api.php?username=Mukti&password=12345&senderid=MUKTIl&route=06&number={mobile}&message={message}&templateid=1507165831296910457')
# print(response)   


import gspread as gs
import pandas as pd

gc = gs.service_account(filename='service_account.json')
import random
import requests
import json
import base64
from ath.info import *
from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError

from copyleaks.models.submit.document import FileDocument
from copyleaks.models.submit.properties.scan_properties import ScanProperties
from copyleaks.models.export import *


def authenticate():
  


    # Authenticating Process
    try:
       auth_token = Copyleaks.login(EMAIL_ADDRESS, KEY) 
       return auth_token
    except CommandError as ce:
            response = ce.get_response()
            print(f"An error occurred (HTTP status code {response.status_code}):")
            print(response.content)
            return "error"








# Use the folowing function to check for AI generated text

def ai_detection(text: str):
    a = authenticate()
    if (a == 'error'):
       return 'Try again later'
    else:
        auth_token = a
        headers = {
       'Content-type': 'application/json',
       'Authorization': f"Bearer {auth_token['access_token']}"
           }
     
        # Submeting and exporting needed data
        scan_id = random.randint(100, 100000)
        try: 
           scan_file = json.dumps({'text':text})
           response = requests.post('https://api.copyleaks.com/v2/writer-detector/{scan_id}/check', headers=headers, data=scan_file)
           txt = response.content
           txt = json.loads(txt)
           results = txt['results']
           isAi = True if results[0]['classification'] == 2 else False
           probapility = str(round(results[0]['probability'] * 100)) + '%'
           msg = "Generated By AI" if isAi else "Free of AI generated content"
           res = dict({'Msg':msg,'Confidence probability':probapility,'isAI':isAi})
           return res
        except KeyError:
                return 'Your text is very short!' 

# Use the following function to scan text for plagiarism

def plagiarism_detection(text:str):
    a = authenticate()
    if (a == 'error'):
       return 'Try again later'
    else:
        auth_token = a
        txt = text.strip()
        BASE64_FILE_CONTENT = base64.b64encode(txt.encode()).decode('utf8')  
        FILENAME = "hello.txt"
        ## Random scan ID
        scan_id = random.randint(100, 100000) 

        ## File Submission Object
        file_submission = FileDocument(BASE64_FILE_CONTENT, FILENAME)

        #it will be modified soon to listen for webhook requests in accordance with frontend
        END_POINT = 'https://webhook.site/7fa0aca0-36af-4ff5-9a15-fe890e28dfb1/86aebc5d-bcf6-4cc6-88f6-8ea08b1a672b'
        #scan_properties = ScanProperties('https://your.server/webhook?event={{STATUS}}')
        scan_properties = ScanProperties(END_POINT)

        ## Scan Properties
        scan_properties.set_sandbox(False)
        file_submission.set_properties(scan_properties)

        # File submitting
        Copyleaks.submit_file(auth_token, scan_id, file_submission) 
        return "Scan done"






if __name__ == "__main__":
    text = "Some costs are incurred only when inflation is unanticipated, while other costs arise even when the inflation is fully anticipated. When unanticipated, price signals can become misinterpreted,and this can reduce economic efficiency. But once individuals adjust to the new higher inflation rate, accurate price signals are restored, and so this cost is only temporary. Only one-time increases in inflation are typically unexpected.Periods of sustained increasing inflation are typically anticipated because when prices rise in one month,individuals and markets may likely anticipate prices to rise in the following month. "
    print(plagiarism_detection(text))
    print(ai_detection(text))
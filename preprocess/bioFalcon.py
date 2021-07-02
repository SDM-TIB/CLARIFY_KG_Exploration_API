# -*- coding: utf-8 -*-

import requests
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}


def get_cui_keyword(text):
    url = 'http://node1.research.tib.eu:9002/umlsmatching?type=cui'
    payload = '{"data":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        return response['cui']
    else:
        return ""
    
    
def get_cui_long(text):
    url = 'http://node1.research.tib.eu:8006/api?mode=long'
    payload = '{"text":"'+text+'"}'
    r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    if r.status_code == 200:
        response=r.json()
        #print(response)
        if len(response['entities_UMLS'])!=0:
            return response['entities_UMLS']
        else:
            return ""
    else:
        return ""
# -*- coding: utf-8 -*-

import requests
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}


def get_cui_keyword(text):
    url = 'https://labs.tib.eu/sdm/biofalcon/api?mode=long'
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
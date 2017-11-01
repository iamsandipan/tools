'''
Created on Aug 11, 2017

@author: sandipan.chakrabarti
'''
from jenkinsapi.jenkins import Jenkins
import requests
import json
from requests.auth import HTTPBasicAuth
jenkinshost = 'http://10.3.44.142:8080'


if __name__ == '__main__':
    resp = requests.get(jenkinshost + '/job/vault-fileservice-synthetic/lastBuild/api/json', auth=HTTPBasicAuth('HQDOMAIN\sandipan.chakrabarti', 'MaManasa12345678#'))
    jsonObj = json.loads(resp.text)
    print(jsonObj['result'])

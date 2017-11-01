'''
Created on Oct 12, 2017

@author: sandipan.chakrabarti
'''
'''
Created on Aug 25, 2017

@author: sandipan.chakrabarti
'''

import boto3
import json
import pprint

session = boto3.session.Session(profile_name='asurion-prod.appadmins', region_name='us-east-1')

client = session.client('cloudwatch')

def getKeyOrNone(key, mapobj):
    if key in mapobj:
        return mapobj[key]
    else:
        return ' '
    
    
if __name__ == "__main__":
    
    paginator = client.get_paginator('describe_alarms')
    i = 0;
    f = open('alarms.txt', 'w')
    for response in paginator.paginate():
        try:
            
            if 'MetricAlarms' in response:
                alarms = response['MetricAlarms']
                for alarm in alarms:
                    
                    if 'AlarmName' in alarm:
                        alarmname = alarm['AlarmName'].lower()
                        if 'pss-vault' in alarmname:
                            i += 1
                            if len(alarm) != 0:
                                f.write(str(alarm) + "\n")
                                f.write(str(getKeyOrNone('OKActions', alarm)) + "\n")
                                f.write(str(getKeyOrNone('AlarmActions', alarm)) + "\n")
                                f.write(str(getKeyOrNone('InsufficientDataActions', alarm)) + "\n")
                                f.write('******************')
                                
                                
        except Exception as ex:
            print(ex)
            print(response)
            #print (response)
            '''
        print(getKeyOrNone('OKActions', alarmdetail))
        print(getKeyOrNone('AlarmActions', alarmdetail))
        print(getKeyOrNone('InsufficientDataActions', alarmdetail))
        '''
    print('Total count')
    print(i)  

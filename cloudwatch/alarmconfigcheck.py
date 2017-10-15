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
    alarmnames=[
            'pss-vault-ecs-cluster-CPU-Down-alarm',
            'pss-vault-fileservice-ext-low-cpu-scaling-alarm',
            'pss-vault-imagedetection-low-cpu-scaling-alarm',
            '[AutoUpdateThreshold]PSS-VAULT-PROD-CBE-FILES-ReadCapacityUnitsLowerLimit-BasicAlarm',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-FLS-AlarmLow-98200d51-b2ed-4d98-b868-a28f9d1a7532',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-FLS-AlarmLow-814a95ca-d524-4106-9650-ad36ed346f0a',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-FLS-AlarmLow-e4f9e0b6-44a8-464e-9311-fc34240aabea',
            'pss-vault-searchservice-int-low-cpu-scaling-alarm',
            'pss-vault-configservice-low-cpu-scaling-alarm',
            'TargetTracking-table/PSS-VAULT-PROD-CSPP-PUBLISHENROLLMENT-KINESIS-AlarmLow-9304e772-a6e6-4cf9-98fa-8c83aa4c74b3',
            'pss-vault-bellprovisioning-low-cpu-scaling-alarm',
            'TargetTracking-table/PSS-VAULT-PROD-CSPP-PUBLISHENROLLMENT-KINESIS-AlarmLow-2b139b68-767b-4e4d-8caa-ae38d63e05b7',
            'pss-vault-droppedenrollment-low-cpu-scaling-alarm',
            'pss-vault-sprintprovisioning-low-cpu-scaling-alarm',
            'pss-vault-reportingservice-ext-low-cpu-scaling-alarm',
            'pss-vault-reportingservice-int-low-cpu-scaling-alarm',
            'PSS-VAULT-PROD-UPLD-FLS-S3EVENTS-DECREASE',
            'PSS-VAULT-PROD-UPLOADED-FILES-S3EVENTS-AUTOTAG',
            'pss-vault-identifyme-low-cpu-scaling-alarm',
            'PSS-VAULT-PROD-CSP-IMAGE-DETECTION-ATTRIBUTES-ReadCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-IMAGE-DETECTION-ATTRIBUTES-ReadCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-THUMB-FAILURE-ReadCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-THUMB-FAILURES-ReadCapacityUnitsLimit-BasicAlarm',
            'pss-vault-nukefiles-low-cpu-scaling-alarm',
            'pss-vault-nukefiles-high-cpu-scaling-alarm',
            'PSS-VAULT-PROD-CGN-CFIGS-rangeKey-index-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-ATS-ENTITY-ReadCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CGN-CFIGS-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-THUMB-FAILURE-WriteCapacityUnitsLimit-BasicAlarm',
            'pss-vault-authenticationservice-ext-low-cpu-scaling-alarm',
            'pss-vault-authenticationservice-ext-high-cpu-scaling-alarm',
            'pss-vault-accountservice-int-low-cpu-scaling-alarm',
            'pss-vault-accountservice-int-high-cpu-scaling-alarm',
            'pss-vault-authenticationservice-int-high-cpu-scaling-alarm',
            'pss-vault-accountservice-ext-high-cpu-scaling-alarm',
            'pss-vault-accountservice-ext-low-cpu-scaling-alarm',
            'pss-vault-authenticationservice-int-low-cpu-scaling-alarm',
            'pss-vault-fileservice-ext-high-cpu-scaling-alarm-NEW',
            'PSS-VAULT-PROD-CAT-IMAGE-DETECTION-ATTRIBUTES-ReadCapacityUnitsLimit-BasicAlarm',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-DATA-AlarmLow-32106d74-d22c-4fb8-bbe6-7e64a154b658',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-DATA-AlarmHigh-7fe168cd-ab0a-4a28-95c6-d854bb6481f6',
            'PSS-VAULT-PROD-CSP-DATA-ReadCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CBE-IMAGE-DETECTION-ATTRIBUTES-ReadCapacityUnitsLimit-BasicAlarm',
            'TargetTracking-table/PSS-VAULT-PROD-SPRINT-ACCOUNT-BACKUP-AlarmLow-ef4ea57f-ba91-4631-a1a4-47dfb89d32ca',
            'TargetTracking-table/PSS-VAULT-PROD-SPRINT-ACCOUNT-BACKUP-AlarmHigh-0db2f5e8-9e21-45da-afd4-4a13e58119f1',
            'TargetTracking-table/PSS-VAULT-PROD-SPRINT-ACCOUNT-BACKUP-AlarmLow-a0cc5d7c-26ad-4017-97c4-4333d092c3e8',
            'TargetTracking-table/PSS-VAULT-PROD-SPRINT-ACCOUNT-BACKUP-AlarmHigh-0e58c287-07de-47ff-8f17-876110e42b6f',
            'PSS-VAULT-PROD-CAT-ACCT-ATTRIBUTES-anchorId-gsi-index-ReadCapacityUnitsLimit-BasicAlarm',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-DATA-AlarmLow-e96d3a9b-bafa-42b3-9e81-bd8280adf3f5',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-DATA-AlarmHigh-02',
            'PSS-VAULT-PROD-CSP-DATA-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-THUMB-FAILURES-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-ATS-ENTITY-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CGN-FLS-WriteCapacityUnitsLimit-BasicAlarm',
            'pss-vault-fileservice-ext-high-cpu-scaling',
            'PSS-VAULT-PROD-IMAGE-DETECTION-ATTRIBUTES-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CBE-IMAGE-DETECTION-ATTRIBUTES-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CBE-FILES-WriteCapacityUnitsLimit-BasicAlarm',
            '[AutoUpdateThreshold]PSS-VAULT-PROD-CBE-FILES-ReadCapacityUnitsLimit-BasicAlarm',
            'pss-vault-ecs-cluster-CPU-Up-alarm',
            'pss-vault-fileservice-ext-high-cpu-scaling-alarm',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-FLS-ProvisionedCapacityLow-98c79d5f-1aca-4c95-b628-79e0736d3752',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-FLS-ProvisionedCapacityHigh-b6402613-c35a-404d-a5f2-b96a0df2758c',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-FLS-AlarmHigh-6e09ef48-cf3f-4b98-b217-da7fea5ea668',
            'PSS-VAULT-PROD-CGN-FLS-ReadCapacityUnitsLimit-BasicAlarm',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-FLS-ProvisionedCapacityLow-124d3598-dbc6-4a0f-98f3-92fa37708f5a',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-FLS-AlarmHigh-57f21bf9-1837-47ff-9dbc-00d8901d6221',
            'TargetTracking-table/PSS-VAULT-PROD-CSP-FLS-ProvisionedCapacityHigh-227513ac-baa1-47e0-a1bf-c6626e60afd2',
            'PSS-VAULT-PROD-CSPP-WORKER-ALARM',
            'pss-vault-searchservice-int-high-cpu-scaling-alarm',
            'pss-vault-configservice-high-cpu-scaling-alarm',
            'TargetTracking-table/PSS-VAULT-PROD-CSPP-PUBLISHENROLLMENT-KINESIS-AlarmHigh-e0e0e6d0-d21c-41df-affe-cd80dde3ad3a',
            'pss-vault-bellprovisioning-high-cpu-scaling-alarm',
            'pss-vault-droppedenrollment-high-cpu-scaling-alarm',
            'TargetTracking-table/PSS-VAULT-PROD-CSPP-PUBLISHENROLLMENT-KINESIS-AlarmHigh-e9b764ed-3f19-44f5-99db-26dc7aadbb8f',
            'PSS-VAULT-PROD-CGN-CFIGS-ReadCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CSP-IMAGE-DETECTION-ATTRIBUTES-WriteCapacityUnitsLimit-BasicAlarm',
            'pss-vault-imagedetection-high-cpu-scaling-alarm',
            'PSS-VAULT-PROD-CAT-IMAGE-DETECTION-ATTRIBUTES-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CGN-CFIGS-rangeKey-index-ReadCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-CSPP-WORKER-ERROR',
            'pss-vault-reportingservice-int-high-cpu-scaling-alarm',
            'pss-vault-reportingservice-ext-high-cpu-scaling-alarm',
            'PSS-VAULT-PROD-UPLD-FLS-S3EVENTS-INCREASE',
            'PSS-VAULT-PROD-CSP-ACCT-ATTRIBUTES-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CAT-FILES-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CAT-FILES-ReadCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CAT-ACCT-ATTRIBUTES-WriteCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CSP-ACCT-ATTRIBUTES-ReadCapacityUnitsLimit-BasicAlarm',
            'PSS-VAULT-PROD-CAT-ACCT-ATTRIBUTES-ReadCapacityUnitsLimit-BasicAlarm',
            'pss-vault-sprintprovisioning-high-cpu-scaling-alarm',
            'TargetTracking-table/PSS-VAULT-PROD-CSPP-PUBLISHENROLLMENT-KINESIS-ProvisionedCapacityHigh-780664e5-1cbc-4448-a747-85d5e39e1cb0',
            'TargetTracking-table/PSS-VAULT-PROD-CSPP-PUBLISHENROLLMENT-KINESIS-ProvisionedCapacityLow-0bea0679-cff0-4cdc-9f7a-619d4dc36211',
            'TargetTracking-table/PSS-VAULT-PROD-CSPP-PUBLISHENROLLMENT-KINESIS-ProvisionedCapacityLow-eaaa7ef4-0caf-41f7-a590-b9abd90aa94a',
            'TargetTracking-table/PSS-VAULT-PROD-CSPP-PUBLISHENROLLMENT-KINESIS-ProvisionedCapacityHigh-700fa146-734a-4bec-be6e-f10ba5dc0b0b',
            'pss-vault-reportingservice-ext-high-cpu-scaling-alarm-NEW',
            'pss-vault-reportingservice-int-high-cpu-scaling-alarm-NEW',
            'pss-vault-identifyme-high-cpu-scaling-alarm',
            'PSS-VAULT-PROD-CAT-ACCT-ATTRIBUTES-anchorId-gsi-index-WriteCapacityUnitsLimit-BasicAlarm',
            'TargetTracking-table/PSS-VAULT-PROD-SPRINT-ACCOUNT-BACKUP-Provision',
            'TargetTracking-table/PSS-VAULT-PROD-SPRINT-ACCOUNT-BACKUP-ProvisionedCapacityLow-07fb5cf6-fbf9-47d7-a99d-dbe3c1816ae2',
            'TargetTracking-table/PSS-VAULT-PROD-SPRINT-ACCOUNT-BACKUP-ProvisionedCapacityHigh-4beda824-2640-4728-8742-7816e69449f1',
            'TargetTracking-table/PSS-VAULT-PROD-SPRINT-ACCOUNT-BACKUP-ProvisionedCapacityHigh-fa9c4d17-f452-47a2-be79-4d9dacc5205f'
        ]
    
    
    for alarm in alarmnames:
        try:
            response = client.describe_alarms(
                AlarmNames=[
                   alarm 
                ]
            )
            
            if 'MetricAlarms' in response:
                alarmdetail = response['MetricAlarms']

                if len(alarmdetail) != 0:
                    alarmdetail = alarmdetail[0]
                    print(alarm)
                    print(getKeyOrNone('OKActions', alarmdetail))
                    print(getKeyOrNone('AlarmActions', alarmdetail))
                    print(getKeyOrNone('InsufficientDataActions', alarmdetail))
                    print('******************')
        except Exception as ex:
            print(ex)
            print(alarm)
            #print (response)
            '''
        print(getKeyOrNone('OKActions', alarmdetail))
        print(getKeyOrNone('AlarmActions', alarmdetail))
        print(getKeyOrNone('InsufficientDataActions', alarmdetail))
        '''
      

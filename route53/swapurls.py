'''
Created on Sep 7, 2017

@author: sandipan.chakrabarti
'''
import boto3
import sys
route53client = boto3.client('route53')
def getHostedZones(dnsName, nextHostedZoneId):
    if nextHostedZoneId is None and dnsName is None:
        return route53client.list_hosted_zones_by_name(
            MaxItems='10',
        ) 
    else:
        return route53client.list_hosted_zones_by_name(
            DNSName=dnsName,
            HostedZoneId = nextHostedZoneId,
            MaxItems='10',
        ) 
        
def getRecordSets(startRecordName, startRecordType, hostedZoneId):
    if startRecordName is None:
        return route53client.list_resource_record_sets(
            HostedZoneId=hostedZoneId,
            MaxItems='10'
        ) 
    else:
        return route53client.list_resource_record_sets(
            HostedZoneId=hostedZoneId,
            StartRecordName = startRecordName,
            StartRecordType = startRecordType,
            MaxItems='10'
        ) 
                
def getChangedRecordSet(name, rectype, ttl, newvalue) :
    changeBatch = {}
    changeBatch.update({'Comment': 'Updated'})
    changes = []
    change = {}
    resourceRecordSet = {}
    resourceRecordSet.update({'Name': name})
    resourceRecordSet.update({'Type': rectype})
    resourceRecordSet.update({'TTL': ttl})
    resourceRecords = []
    resourceRecord = {'Value':newvalue}
    resourceRecords.append(resourceRecord)
    resourceRecordSet.update({'ResourceRecords':resourceRecords})
    change.update({'Action': 'UPSERT'})
    change.update({'ResourceRecordSet': resourceRecordSet})
    changes.append(change)
    changeBatch.update({'Changes':changes})
    return changeBatch

def findRecordSet(recordSetUrl, recordSetType):
    isTruncated = True;
    nextRecordName = None
    while(isTruncated):
        response = getRecordSets(nextRecordName, recordSetType, hostedZoneId)
        isTruncated = response['IsTruncated']
        if 'NextRecordName' in response:
            nextRecordName = response['NextRecordName']

        resourceRecords = response['ResourceRecordSets']
        for resourceRecord in resourceRecords: 
            if resourceRecord['Name'] == recordSetUrl + '.' and resourceRecord['Type'] == recordSetType:
                    return resourceRecord 

    return None 

def getHostedZoneId(hostedzonename): 
    istruncated = True
    nextHostedZoneId = None
    nextDNSName = None
    while(istruncated):
        response = getHostedZones(nextDNSName, nextHostedZoneId)
        istruncated = response['IsTruncated']
        hostedzones = response['HostedZones']
        
        if 'NextHostedZoneId' in response:
            nextHostedZoneId = response['NextHostedZoneId']
        
        if 'NextDNSName' in response:
            nextDNSName = response['NextDNSName']
            
        for hostedzone in hostedzones:
            if hostedzone['Name'] == hostedzonename:
                return hostedzone['Id']
    
    return None    

        
if __name__=="__main__":
    env = sys.argv[1]
    hostedzoneName = sys.argv[2]
    recordSetName = sys.argv[3]
    recordSetType = sys.argv[4]
    newUrl = sys.argv[5]
    session = boto3.session.Session(profile_name=env, region_name='us-east-1')
    
    '''
    hostedzoneName = 'asurionpa.com.'
    recordSetName = 'hello-svc-memories.asurionpa.com'
    recordSetType = 'CNAME'
    newUrl = 'helloworld-3-alb-1052942687.us-east-1.elb.amazonaws.com'
    '''
    
    hostedZoneId=getHostedZoneId(hostedzoneName)
    recordset = findRecordSet(recordSetName, recordSetType)
    
    if recordset is None:
        raise Exception('RecordSet Not found')
    
    name = recordset['Name'] 
    rectype = recordset['Type']
    ttl = recordset['TTL']
    changeBatch = getChangedRecordSet(name, rectype, ttl, newUrl)
    print(recordset) 
    
    try: 
            response = route53client.change_resource_record_sets(
                HostedZoneId=hostedZoneId,
                ChangeBatch=changeBatch
            )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print('Route 53 Update request submitted successfully')
            print("Record set updated to point to : " + newUrl)
    except Exception as e:
        print( e)
     
    

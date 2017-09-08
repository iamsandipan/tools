'''
Created on Sep 7, 2017

@author: sandipan.chakrabarti
'''
import boto3
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
        
        
        
        
if __name__=="__main__":
    istruncated = True
    nextHostedZoneId = None
    nextDNSName = None
    zones = {}
    while(istruncated):
        response = getHostedZones(nextDNSName, nextHostedZoneId)
        istruncated = response['IsTruncated']
        hostedzones = response['HostedZones']
        if 'NextHostedZoneId' in response:
            nextHostedZoneId = response['NextHostedZoneId']
        
        if 'NextDNSName' in response:
            nextDNSName = response['NextDNSName']
            
        for hostedzone in hostedzones:
            zones.update({hostedzone['Name']: hostedzone['Id']})
    
    
    response = route53client.list_resource_record_sets(
        HostedZoneId=zones.get('asurionpa.com.')
    )
    
    print(response)
'''
Created on Sep 12, 2017

@author: sandipan.chakrabarti
'''
from mixpanel import Mixpanel
mp = Mixpanel('664ffe7a8bdf85207bda500ac4251485')
import boto3
if __name__ == "__main__":
    env = 'asurion-sqa.pspdevops'
    session = boto3.session.Session(profile_name=env, region_name='us-east-1')
    searchclient = session.client('cloudsearchdomain')
    query = '(and file_type:\'image/jpeg\')'
    response = searchclient.search(
                        query = 'pss-vault-qa-cgn-cs',
                        queryParser='structured',          
                )
    print (response)
    '''
    resp = mp.track('OperationalMetrics_Memories', 'OperationalMetrics_Memories', {
        'TotalFiles': '100',
        'TotalPhotos': '200',
        'TotalVideos' : '300'
    })
    '''
    print ('Send to Mixpanel')

# You can also include properties to describe
# the circumstances of the event

'''
Created on Sep 12, 2017

@author: sandipan.chakrabarti
'''
import mixpanel
from mixpanel import Mixpanel
mp = Mixpanel('664ffe7a8bdf85207bda500ac4251485')
import boto3

DOMAIN_URL='http://search-pss-vault-qa-cgn-cs-dkvcsd52efuifgkagv4dg4ckiq.us-east-1.cloudsearch.amazonaws.com'
def getHitCount(query):
    response = searchclient.search(
                        query = query,
                        queryParser='structured'
                )
    return response['hits']['found']

if __name__ == "__main__":
    env = 'SQA'
    session = boto3.session.Session(profile_name=env, region_name='us-east-1')
    searchclient = session.client('cloudsearchdomain', endpoint_url=DOMAIN_URL)
    
    videoquery = 'file_type: \'video\''
    videos = getHitCount(videoquery)
    
    imagequery = 'file_type: \'image\''
    images = getHitCount(imagequery)
                
    print (videos)
    print (images)
    
    
    
    resp = mp.track('OperationalMetrics_Memories', 'OperationalMetrics_Memories', {
        'TotalPhotos': images,
        'TotalVideos' : videos
    })
    print ('Send to Mixpanel')

# You can also include properties to describe
# the circumstances of the event

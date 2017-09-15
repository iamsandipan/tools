'''
Created on Sep 12, 2017

@author: sandipan.chakrabarti
'''
import mixpanel
import boto3
import datetime
import sys

from mixpanel import Mixpanel
mp = Mixpanel('664ffe7a8bdf85207bda500ac4251485')

DOMAIN_URL='http://search-pss-vault-prod-csp-cs-wikr7mxllygo2gpubeicxrruwq.us-east-1.cloudsearch.amazonaws.com'

def fireStructuredQuerywithstatus(query):
    response = searchclient.search(
                        query = query,
                        facet = '{"file_state":{"buckets":["PENDING"]}}',
                        queryParser='structured',
                )
    print(response)
    return response['stats']['file_size']


def fireStructuredQuerywithstats(query):
    response = searchclient.search(
                        query = query,
                        queryParser='structured',
                        stats='{"file_size":{}}'
                )
    return response['stats']['file_size']

def fireStructuredQuery(query):
    response = searchclient.search(
                        query = query,
                        queryParser='structured'
                )
    return response['hits']['found']

def getFileStatus(filetype):
    now = (datetime.datetime.now())
    starttime = datetime.datetime(now.year, now.month, now.day -1 , 0, 0, 0).strftime('%s000')
    endtime = datetime.datetime(now.year, now.month, now.day , 0, 0, 0).strftime('%s000')
    query = '(and file_type:\''+ filetype + '\' (and (range field=file_creation_date ['+ starttime +','+ endtime +'])))'
    return fireStructuredQuerywithstatus(query) 

def getFileStats(filetype):
    now = (datetime.datetime.now())
    starttime = datetime.datetime(now.year, now.month, now.day -1 , 0, 0, 0).strftime('%s000')
    endtime = datetime.datetime(now.year, now.month, now.day , 0, 0, 0).strftime('%s000')
    query = '(and file_type:\''+ filetype + '\' (and (range field=file_creation_date ['+ starttime +','+ endtime +'])))'
    return fireStructuredQuerywithstats(query) 

def getPreviousDayVideoCount():
    now = (datetime.datetime.now())
    starttime = datetime.datetime(now.year, now.month, now.day  - 1, 0, 0, 0).strftime('%s000')
    endtime = datetime.datetime(now.year, now.month, now.day, 0, 0, 0).strftime('%s000')
    query = '(and file_type:\'video\' (and (range field=file_creation_date ['+ starttime +','+ endtime +'])))'
    return fireStructuredQuery(query)  

def getPreviousDayImageCount():
    now = (datetime.datetime.now())
    starttime = datetime.datetime(now.year, now.month, now.day - 1, 0, 0, 0).strftime('%s000')
    endtime = datetime.datetime(now.year, now.month, now.day , 0, 0, 0).strftime('%s000')
    query = '(and file_type:\'image\' (and (range field=file_creation_date ['+ starttime +','+ endtime +'])))'
    return fireStructuredQuery(query)  

    
def fireSimpleQuery(query):
    response = searchclient.search(
                        query = query
                )
    return response['hits']['found']

if __name__ == "__main__":
    env = sys.argv[1]
    print(env)
    session = boto3.session.Session(profile_name=env, region_name='us-east-1')
    searchclient = session.client('cloudsearchdomain', endpoint_url=DOMAIN_URL)
    
    print ('Previous Day Counts ')
    videostats = getFileStats('video')
    photostats = getFileStats('image')
    
    totalVideos = videostats['count']
    print('Total Videos' + str(totalVideos))
    totalPhotos = photostats['count']
    print('Total Photos' + str(totalPhotos))
    totalFiles = totalVideos + totalPhotos
    print('Total Files' + str(totalFiles))

    
    totalFileSizeUploaded = int(((videostats['sum'] + photostats['sum']))/(1024*1024*1024))
    print('Total Uploaded GB' + str(totalFileSizeUploaded))
    totalPhotoSize = int(photostats['sum']/(1024*1024*1024))
    print('Photo Uploaded GB' + str(totalPhotoSize))
    totalVideoSize = int(videostats['sum']/(1024*1024*1024))
    print('Video Uploaded GB' + str(totalVideoSize))
    
    resp = mp.track('OperationalMetrics_Memories', 'OperationalMetrics_Memories', {
        'TotalPhotos' : totalFiles,
        'TotalPhotos': totalPhotos,
        'TotalVideos' : totalVideos,
        'TotalFilesSizeUploadedInGB':totalFileSizeUploaded,
        'TotalPhotoSizeUploadedInGB':totalPhotoSize,
        'TotalVideoSizeUploadedInGB':totalVideoSize
    })
    print ('Send to Mixpanel')

# You can also include properties to describe
# the circumstances of the event

'''
Created on Sep 12, 2017

@author: sandipan.chakrabarti f1 adding something to f1


'''
import mixpanel
import boto3
import datetime
import sys

from mixpanel import Mixpanel
mp = Mixpanel('664ffe7a8bdf85207bda500ac4251485')
#file_state 
DOMAIN_URL_SPRINT='http://search-pss-vault-prod-csp-cs-wikr7mxllygo2gpubeicxrruwq.us-east-1.cloudsearch.amazonaws.com'
DOMAIN_URL_AFF='http://search-pss-vault-prod-cs-ss-pat5th5dkjym5sexzo4yg2fkxy.us-east-1.cloudsearch.amazonaws.com'


def fireStructuredQuerywithstats(query, searchclient):
    response = searchclient.search(
                        query = query,
                        queryParser='structured',
                        stats='{"file_size":{}}'
                )
    stats = response['stats']
    if 'file_size' in stats:
        return stats['file_size']
    else:
        print('Returning None')
        return None


def getFileStats(filetype, searchclient):
    now = (datetime.datetime.now())
    starttime = datetime.datetime(now.year, now.month, now.day -1 , 0, 0, 0).strftime('%s000')
    endtime = datetime.datetime(now.year, now.month, now.day , 0, 0, 0).strftime('%s000')
    query = '(and file_type:\''+ filetype + '\' (and (range field=file_creation_date ['+ starttime +','+ endtime +'])))'
    return fireStructuredQuerywithstats(query, searchclient) 

def collectStats(carrier, searchclient):
    print('Previous Day Counts ')
    videostats = getFileStats('video', searchclient)
    photostats = getFileStats('image', searchclient)
    
    totalVideos = 0
    if 'count' in videostats:
        totalVideos = videostats['count']
        print('Total Videos : ' + str(totalVideos))
    totalPhotos = 0
    if 'count' in photostats:
        totalPhotos = photostats['count']
        print('Total Photos :' + str(totalPhotos))
     
    totalFiles = totalVideos + totalPhotos
    print('Total Files' + str(totalFiles))

    totalPhotoSize = 0
    if 'sum' in photostats:
        totalPhotoSize = int(photostats['sum'] / (1024 * 1024 * 1024))
        print('Photo Uploaded GB' + str(totalPhotoSize))
        
    totalVideoSize = 0
    if 'sum' in videostats:
        totalVideoSize = int(videostats['sum'] / (1024 * 1024 * 1024))
        print('Video Uploaded GB' + str(totalVideoSize))
        
    totalFileSizeUploaded = int((totalVideoSize + totalPhotoSize) / (1024 * 1024 * 1024))
    print('Total Uploaded GB' + str(totalFileSizeUploaded))
    
    '''
    mp.track('OperationalMetrics_Memories', 'OperationalMetrics_Memories', {
            'CarrierId': carrier, 
            'TotalFiles':totalFiles, 
            'TotalPhotos':totalPhotos, 
            'TotalVideos':totalVideos, 
            'TotalFilesSizeUploadedInGB':totalFileSizeUploaded, 
            'TotalPhotoSizeUploadedInGB':totalPhotoSize, 
            'TotalVideoSizeUploadedInGB':totalVideoSize})
    '''
if __name__ == "__main__":
    env = sys.argv[1]
    print(env)
    session = boto3.session.Session(profile_name=env, region_name='us-east-1')
    sprintclient = session.client('cloudsearchdomain', endpoint_url=DOMAIN_URL_SPRINT)
    
    session = boto3.session.Session(profile_name=env, region_name='us-east-1')
    affclient = session.client('cloudsearchdomain', endpoint_url=DOMAIN_URL_AFF)
    
    collectStats('SPRINT', sprintclient)
    collectStats('AFF', affclient)
    print ('Send to Mixpanel')

# You can also include properties to describe
# the circumstances of the event

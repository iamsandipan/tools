'''
Created on Sep 12, 2017

@author: sandipan.chakrabarti
'''
from mixpanel import Mixpanel
mp = Mixpanel('664ffe7a8bdf85207bda500ac4251485')

if __name__ == "__main__":
    resp = mp.track('OperationalMetrics_Memories', 'OperationalMetrics_Memories', {
        'TotalFiles': '100',
        'TotalPhotos': '200',
        'TotalVideos' : '300'
    })

    print ('Send to Mixpanel')

# You can also include properties to describe
# the circumstances of the event

'''
Created on Sep 12, 2017

@author: sandipan.chakrabarti
'''
import mixpanel
from mixpanel import Mixpanel
mp = Mixpanel('664ffe7a8bdf85207bda500ac4251485')



# You can also include properties to describe
# the circumstances of the event
mp.track('11111111111111111111111', 'Memories_OperationalMetrics', {
    'TotalFiles': '100'
})
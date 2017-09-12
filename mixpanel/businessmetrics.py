'''
Created on Sep 12, 2017

@author: sandipan.chakrabarti
'''
import mixpanel
from mixpanel import Mixpanel
mp = Mixpanel('664ffe7a8bdf85207bda500ac4251485')

# Tracks an event, 'Sent Message',
# with distinct_id user_id
mp.track('11111111111111111111111', 'Sent Message')

# You can also include properties to describe
# the circumstances of the event
mp.track('11111111111111111111111', 'Plan Upgraded', {
    'Old Plan': 'Business',
    'New Plan': 'Premium'
})
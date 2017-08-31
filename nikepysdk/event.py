class NikeEvent(object):
    def __init__(self, event_data):
        self.title = event_data['event']['eventDetails'][0]['name']
        self.event_id = event_data['event']['id']
        self.capacity = event_data['event']['capacity']
        self.registration_count = event_data['event']['registrationCount']
        self.location = event_data['event']['eventLocation']['name']
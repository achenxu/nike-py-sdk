class NikeEvent(object):
    def __init__(self, event_data):
        event_data = event_data.get('event', event_data)
        try:
            self.title = event_data['eventDetails'][0]['name']
        except KeyError:
            self.title = event_data['name']
        self.event_id = event_data['id']
        self.capacity = event_data['capacity']
        self.registration_count = event_data['registrationCount']
        try:
            self.location = event_data['eventLocation']['name']
        except KeyError:
            self.location = event_data['locationName']

class NikeSeries(object):
    def __init__(self, series_data):
        self.title = series_data['multiPage']['name']
        self.events = [NikeEvent(x) for x in series_data['multiPage']['events']]
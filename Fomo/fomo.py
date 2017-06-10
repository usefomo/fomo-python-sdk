import json

import requests

try:
    import ssl
except ImportError:
    print('error: no ssl support')
    exit(1)


class FomoClient:
    """Fomo Client wrapper"""

    def __init__(self, token):
        """Initializes client with authorization token"""
        #: Fomo API auth token
        self.__token = token

        #: Fomo API endpoint
        self.__endpoint = 'https://www.usefomo.com'

        #: SDK version
        self.__version__ = '1.0.4'

    def get_event(self, event_id):
        """Get Fomo Event

        @:param event_id: Fomo Event ID
        :return: :class:`FomoEvent <FomoEvent>` object
        :rtype: FomoEvent

        """
        return FomoEvent.from_json(self.__makeRequest('/api/v1/applications/me/events/' + repr(event_id), 'GET'))

    def get_events(self, size=30, page=1):
        """Get Fomo events

        :return: :class:`FomoEventList <FomoEventList>` object
        :rtype: FomoEventList

        """
        return FomoEvent.list_from_json(
            self.__makeRequest('/api/v1/applications/me/events?per=' + repr(size) + '&page=' + repr(page), 'GET'))

    def get_events_with_meta(self, size=30, page=1):
        """Get Fomo events with meta data

        :return: :class:`FomoEventsWithMeta <FomoEventsWithMeta>` object
        :rtype: FomoEventsWithMeta

        """
        response = self.__makeRequest(
            '/api/v1/applications/me/events?per=' + repr(size) + '&page=' + repr(page) + '&show_meta=true', 'GET')
        return FomoEventsWithMeta.from_json(response)

    def delete_event(self, event_id):
        """Delete Fomo Event

        @:param event_id: string Fomo Event ID
        :return: :class:`FomoDeleteMessageResponse <FomoDeleteMessageResponse>` object
        :rtype: FomoDeleteMessageResponse

        """
        return FomoDeleteMessageResponse.from_json(
            self.__makeRequest('/api/v1/applications/me/events/' + repr(event_id), 'DELETE'))

    def create_event(self, event):
        """Create Fomo Event

        @:param event: Fomo event to create
        @type event: FomoEventBasic
        :return: :class:`FomoEvent <FomoEvent>` object
        :rtype: FomoEvent

        """
        return FomoEvent.from_json(
            self.__makeRequest('/api/v1/applications/me/events', 'POST', FomoEventWrapper(event)))

    def update_event(self, event):
        """Update Fomo Event

        @:param event: Fomo event to update
        @type event: FomoEvent
        :return: :class:`FomoEvent <FomoEvent>` object
        :rtype: FomoEvent

        """
        return FomoEvent.from_json(
            self.__makeRequest('/api/v1/applications/me/events/' + repr(event.id), 'PATCH', FomoEventWrapper(event)))

    def __makeRequest(self, path, method, data=None):
        """Make Fomo Authorized API request

        @:param path: API path
        @type path: string
        @:param method: HTTP method
        @type method: string
        @:param data: Dictionary of data to be send to server
        @type data: FomoEventWrapper

        """
        headers = {
            'Authorization': 'Token ' + self.__token,
            'User-Agent': 'Fomo/Python/' + self.__version__
        }
        if data is not None:
            headers['Content-Type'] = 'application/json'

        response = requests.request(method, self.__endpoint + path,
                                    data=data.to_JSON() if data is not None else None,
                                    headers=headers)
        return response.text


class FomoEventCustomAttribute(object):
    """Custom event attribute"""

    def __init__(self, key, value):
        """Creates new custom attribute object"""
        #: Custom attribute key
        self.key = key

        #: Custom attribute value
        self.value = value

    def __str__(self):
        """Dumps JSON serialized object"""
        return json.dumps(self.__dict__, indent=4)


class FomoEventBasic(object):
    """Fomo basic event"""

    def __init__(self, event_type_id="", event_type_tag="", url="", first_name="", email_address="", ip_address="", city="", province="", country="",
                 title="",
                 image_url="", custom_event_fields_attributes=None):
        """Create a new Fomo basic event"""

        #: Event type unique ID (optional|required if event_type_tag = '')
        if custom_event_fields_attributes is None:
            custom_event_fields_attributes = []
        self.event_type_id = event_type_id

        #: Event type tag (optional|required if event_type_id = '')
        self.event_type_tag = event_type_tag

        #: Url to redirect on the event click. Size range: 0..255 (required)
        self.url = url

        #: First name of the person on the event. Size range: 0..255
        self.first_name = first_name

        #: Email address of the person on the event. Size range: 0..255
        self.email_address = email_address

        #: IP address of the person on the event. Size range: 0..255
        self.ip_address = ip_address

        #: City where the event happened. Size range: 0..255
        self.city = city

        #: Province where the event happened. Size range: 0..255
        self.province = province

        #: Country where the event happened ISO-2 standard. Size range: 0..255
        self.country = country

        #: Title of the event. Size range: 0..255
        self.title = title

        #: Url of the image to be displayed. Size range: 0..255
        self.image_url = image_url

        #: A list of :class:`FomoEventCustomAttribute <FomoEventCustomAttribute>` objects for custom event fields
        self.custom_event_fields_attributes = custom_event_fields_attributes

    def add_custom_event_field(self, key, value):
        """Add custom event field"""
        self.custom_event_fields_attributes.append(FomoEventCustomAttribute(key, value))

    def __str__(self):
        """Dumps JSON serialized object"""
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        """Parse object from JSON"""
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)

    def __repr__(self):
        """Dumps itself to dictionary"""
        return json.dumps(self.__dict__)


class FomoEvent(FomoEventBasic):
    """Fomo event"""

    def __init__(self, event_type_id="", event_type_tag="", url="", first_name="", email_address="", ip_address="", city="", province="", country="",
                 title="",
                 image_url="", custom_event_fields_attributes=None, id="", created_at="", updated_at="", message="",
                 link="", application_id="", created_at_to_seconds_from_epoch=None, template_vars=None):
        """Creates new Fomo event object"""
        if custom_event_fields_attributes is None:
            custom_event_fields_attributes = []
        FomoEventBasic.__init__(self, event_type_id, event_type_tag, url, first_name, email_address,
                                ip_address, city, province, country, title, image_url,
                                custom_event_fields_attributes)

        #: Id of the event type (needed only for the update)
        self.id = id

        #: Application ID (received info)
        self.application_id = application_id

        #: Created at seconds from epoch
        self.created_at_to_seconds_from_epoch = created_at_to_seconds_from_epoch

        #: Created timestamp (received info)
        self.created_at = created_at

        #: Updated timestamp (received info)
        self.updated_at = updated_at

        #: Message template (received info)
        self.message = message

        #: Full link (received info)
        self.link = link

        #: Used template variables
        self.template_vars = template_vars

    def __str__(self):
        """Dumps JSON serialized object"""
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        """Parse object from JSON"""
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    @classmethod
    def list_from_json(cls, json_str):
        """Parse objects from JSON"""
        json_dict = json.loads(json_str)
        event_list = []
        for obj in json_dict:
            event_list.append(cls(**obj))

        return FomoEventList(event_list)

    def __repr__(self):
        """Dumps itself to dictionary"""
        return json.dumps(self.__dict__)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)


class FomoEventList(list):
    """List of Fomo Events"""

    def __str__(self):
        """Dumps JSON serialized objects"""
        return json.dumps([ob.__dict__ for ob in self], indent=4)

    def __getitem__(self, item):
        """Returns Fomo event item

        :return: :class:`FomoEvent <FomoEvent>` object
        :rtype: FomoEvent

        """
        return item

    def __repr__(self):
        """Dumps itself to dictionary"""
        return json.dumps(self.__dict__)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)


class FomoEventsMeta(object):
    def __init__(self, per_page=30, page=1, total_count=0, total_pages=1):
        """Initializes Fomo Events Meta"""

        #: Page size
        self.per_page = per_page

        #: Page number
        self.page = page

        #: Total count
        self.total_count = total_count

        #: Total pages
        self.total_pages = total_pages;

    def __str__(self):
        """Dumps JSON serialized object"""
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        """Parse object from JSON"""
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def __repr__(self):
        """Dumps itself to dictionary"""
        return json.dumps(self.__dict__)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)


class FomoEventsWithMeta(object):
    def __init__(self, events=None, meta=None):
        """Initializes Fomo Events with Meta"""
        #: Events
        if events is None:
            events = []
        self.events = events
        #: Meta data
        self.meta = meta

    def __str__(self):
        """Dumps JSON serialized object"""
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        """Parse object from JSON"""
        json_dict = json.loads(json_str)
        cls.events = FomoEvent.list_from_json(json.dumps(json_dict['events']))
        cls.meta = FomoEventsMeta.from_json(json.dumps(json_dict['meta']))
        return cls

    def __repr__(self):
        """Dumps itself to dictionary"""
        return json.dumps(self.__dict__)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)


class FomoDeleteMessageResponse(object):
    """Fomo Delete Event response"""

    def __init__(self, message=None):
        """Initializes Fomo Delete Event object"""
        #: Message
        self.message = message

    def __str__(self):
        """Dumps JSON serialized object"""
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        """Parse object from JSON"""
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def __repr__(self):
        """Dumps itself to dictionary"""
        return json.dumps(self.__dict__)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)


class FomoEventWrapper(object):
    def __init__(self, event=None):
        """Initializes Fomo Event wrapper"""
        #: Event
        self.event = event

    def __str__(self):
        """Dumps JSON serialized object"""
        return json.dumps(self.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        """Parse object from JSON"""
        json_dict = json.loads(json_str)
        return cls(**json_dict)

    def __repr__(self):
        """Dumps itself to dictionary"""
        return json.dumps(self.__dict__)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)

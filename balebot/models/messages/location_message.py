import json as json_handler
from balebot.models.base_models.location import Location
from balebot.models.messages.base_message import BaseMessage
from balebot.models.constants.errors import Error
from balebot.models.constants.message_type import MessageType


class LocationMessage(BaseMessage):
    def __init__(self, latitude, longitude):
        self.raw_json = Location(latitude=latitude, longitude=longitude)

    def get_json_object(self):

        data = {
            "$type": MessageType.json_message,
            "rawJson": self.raw_json.get_json_str()
        }
        return data

    def get_json_str(self):
        return json_handler.dumps(self.get_json_object())

    @classmethod
    def load_from_json(cls, json):
        if isinstance(json, dict):
            json_dict = json
        elif isinstance(json, str):
            json_dict = json_handler.loads(json)
        else:
            raise ValueError(Error.unacceptable_json)
        latitude = json_dict.get('latitude', None)
        longitude = json_dict.get('longitude', None)

        if (not latitude) or (not longitude):
            raise ValueError(Error.none_or_invalid_attribute)

        return cls(latitude=latitude, longitude=longitude)

import json
import requests
from requests.auth import HTTPBasicAuth
from arklex.env.tools.tools import register_tool, logger
from arklex.env.tools.acuity.utils import EXCEPTIONS

description = "Get the available times of the info session based on the specific date"
slots = [
    {
        "name": "date",
        "type": "string",
        "description": "The date of the info session the user wants to attend. It should consist of year, month, day. e.g. 2025-04-12. If you are not sure about the user's input, ask them to confirm.",
        "prompt": "",
        "required": True,
    },
    {
        "name": "apt_id",
        "type": "string",
        "description": "The appointment id of the info session and it should be consisted of numbers. e.g. 76474933",
        "prompt": "Which info session would you like to attend?",
        "required": True,
    }
]
outputs = [
    {
        "name": "time_ls",
        "type": "string",
        "description": "The available times of the specific info session",
    }
]
CREDENTIAL_NOT_FOUND = 'error: missing credential information'
errors = [
    EXCEPTIONS
]

@register_tool(description, slots, outputs, lambda x: x not in errors)
def get_available_times(date, apt_id, **kwargs):
    user_id = kwargs.get('ACUITY_USER_ID')
    api_key = kwargs.get('ACUITY_API_KEY')
    if not api_key or not user_id:
        return CREDENTIAL_NOT_FOUND

    base_url = 'https://acuityscheduling.com/api/v1/availability/times?appointmentTypeID={}&date={}'.format(apt_id, date)
    response = requests.get(base_url, auth=HTTPBasicAuth(user_id, api_key))

    if response.status_code == 200:
        data = response.json()
        return json.dumps(data)
    else:
        return EXCEPTIONS
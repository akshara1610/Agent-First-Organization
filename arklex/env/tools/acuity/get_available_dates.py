import json
import requests
from requests.auth import HTTPBasicAuth
from arklex.env.tools.tools import register_tool, logger
from arklex.env.tools.acuity.utils import EXCEPTIONS

description = "Get the available dates of the info session based on the specific month"
slots = [
    {
        "name": "year",
        "type": "string",
        "description": "The current year. If you are not sure, you could ask the user to confirm. e.g. 2025",
        "prompt": "",
        "required": True,
    },
    {
        "name": "month",
        "type": "string",
        "description": "The month of the available info session held by the organization. e.g. January, 1, Jan. If you have known the date, transform to 01.",
        "prompt": "Could you please give me the month you want to attend the info session?",
        "required": True,
    },
    {
        "name": "apt_name",
        "type": "string",
        "description": "The appointment name of the info session. It allow user to input some parts of the name, but if you are unsure, ask the user to confirm.",
        "prompt": "Which info session would you like to attend?",
        "required": True,
    },
    {
        "name": "session_types",
        "type": "string",
        "description": "ll available information sessions types",
        "prompt": "",
        "required": True,
    },
]
outputs = [
    {
        "name": "date_ls",
        "type": "string",
        "description": "The available date of the specific info session in this specific month",
    },
    {
        "name": "apt_id",
        "type": "string",
        "description": "The id of the info session",
    }

]
CREDENTIAL_NOT_FOUND = 'error: missing credential information'
errors= [
    EXCEPTIONS
]

@register_tool(description, slots, outputs, lambda x: x not in errors)
def get_available_date(year, month, apt_name, session_types, **kwargs):
    user_id = kwargs.get('ACUITY_USER_ID')
    api_key = kwargs.get('ACUITY_API_KEY')
    if not api_key or not user_id:
        return CREDENTIAL_NOT_FOUND
    session_types = json.loads(session_types)
    session = [session for session in session_types if session.get("name") == apt_name]
    apt_id = session[0].get("id")

    base_url = 'https://acuityscheduling.com/api/v1/availability/dates?appointmentTypeID={}1&month={}'.format(apt_id, year + '-' + month)
    response = requests.get(base_url, auth=HTTPBasicAuth(user_id, api_key))

    if response.status_code == 200:
        data = response.json()
        return json.dumps(data), apt_id
    else:
        return EXCEPTIONS
import json
import logging

import datetime
import jsonschema
from dateutil.parser import parse
from jsonschema import validate

from app import app

mySchema = {
  "type": "object",
  "properties": {
    "Store": {
      "type": "integer"
    },
    "DayOfWeek": {
      "type": "integer"
    },
    "Date": {
      "type": "string"
    },
    "Customers": {
      "type": "integer"
    },
    "Open": {
      "type": "integer"
    },
    "Promo": {
      "type": "integer"
    },
    "StateHoliday": {
      "type": "string"
    },
    "SchoolHoliday": {
      "type": "integer"
    }
  },
  "required": [
    "Store",
    "DayOfWeek",
    "Date",
    "Customers",
    "Open",
    "Promo",
    "StateHoliday",
    "SchoolHoliday"
  ]
}

def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=mySchema)
        validate_date(jsonData["Date"])
    except jsonschema.exceptions.ValidationError:
        logging.exception("Invalid json")
        return False
    except ValueError as e:
        logging.exception("Exception " + str(e))
        return False
    return True


def validate_date(date_text):
  try:
      datetime.datetime.strptime(date_text, '%Y-%m-%d')
  except ValueError:
      raise ValueError("Incorrect data format, should be YYYY-MM-DD")

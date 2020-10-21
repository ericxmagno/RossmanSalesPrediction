import json
import logging

import jsonschema
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
    except jsonschema.exceptions.ValidationError:
        logging.exception("Invalid json")
        return False
    return True
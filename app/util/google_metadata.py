# -*- coding: utf-8 -*-
from typing import Dict

from google.cloud import runtimeconfig
from google.cloud.runtimeconfig.config import Config


def get_project_attributes() -> Dict[str, str]:
    """Gets the directory of custom metadata values for this project
    from the Runtime Configuration API.
    """
    result = {}
    config_client = runtimeconfig.Client()
    config: Config = config_client.config('app-production')
    list_variables = config.list_variables()
    for variable in list_variables:
        variable.reload()
        result[variable.name] = variable.value.decode('utf-8')
    return result

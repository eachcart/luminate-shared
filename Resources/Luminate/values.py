#   ██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗ █████╗ ████████╗███████╗
#   ██║     ██║   ██║████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██╔════╝
#   ██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║███████║   ██║   █████╗  
#   ██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██║   ██║   ██╔══╝  
#   ███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ███████╗
#   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
#
#   © eachcart • 2025
#   Licensed under ePL.
#   https://github.com/eachcart/ePL

import json
from Resources.Luminate.psc import PSCParser
psc = PSCParser()

with open("Resources/userconfig.psc", "r", encoding="utf-8") as config:
        config = psc.parse(config.read())

_CURRENT = config["misc"]["current"]
_VERSION = config[_CURRENT]["version"]
_BUILD = config[_CURRENT]["build"]
_BRANCH = config[_CURRENT]["branch"]
_FRAMEWORK = config[_CURRENT]["framework"]
_PREFIX = config[_CURRENT]["prefix"]
_INFO_PATH = config[_CURRENT]["info_path"]

_IMAGE_PATH = config[_CURRENT]["image_path"]
_IMAGE_PATH_SMALL = config[_CURRENT]["image_path_small"]

_API_ID = config[_CURRENT]["credentials"]["api_id"]
_API_HASH = config[_CURRENT]["credentials"]["api_hash"]
_SESSION = config[_CURRENT]["credentials"]["session"]

_MILENIUM = config["misc"]["milenium"]
_ASB_SLEEP_MIN = config["misc"]["asb_sleep_min"]
_ASB_SLEEP_MAX = config["misc"]["asb_sleep_max"]

custom_commands = {}
system_commands = {
    'info': ("Информация о юзерботе."),
    'help': ("Все доступные команды."),
    'milenium, m': ("Milenium. (репозиторий Luminate)"),
    'lm': ("Загрузить .py модуль. (Реплай)"),
    'unlm': ("Выгрузить .py модуль."),
    'dlm': ("Скачать и загрузить .py модуль."),
    'lumi, l + reload,rst / shutdown,off': ("Управление юзерботом."),
}
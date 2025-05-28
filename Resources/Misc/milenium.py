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

import requests, json
from Resources.Luminate.values import _MILENIUM

class Milenium:
    @classmethod
    def fetch(cls):
        try:
            response = requests.get(_MILENIUM, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Ошибка загрузки данных Milenium: {e}")
            return {}

    @classmethod
    def search(cls, query):
        data = cls.fetch()
        results = []

        if not data:
            return "❌ База данных недоступна."

        query = query.lower()
        for package, info in data.items():
            if query in package.lower() or any(query in cmd for cmd in info.get("commands", {})):
                results.append((package, info))

        return results if results else "404 ❌ Ничего не найдено."

    @classmethod
    def get_package(cls, package_name):
        data = cls.fetch()
        return data.get(package_name, "404 ❌ Пакет не найден.")

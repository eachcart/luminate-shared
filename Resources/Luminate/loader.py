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

import importlib.util, os, traceback

loaded_modules = []

def LoadModules(commands, lumi):
    modules_path = "Resources/Modules"
    loaded = 0

    if not os.path.isdir(modules_path):
        print(f"[!] Папка '{modules_path}' не найдена.")
        return

    for filename in os.listdir(modules_path):
        if not filename.endswith(".py") or filename.startswith("_"):
            continue

        module_name = filename[:-3]
        module_path = os.path.join(modules_path, filename)

        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if not spec or not spec.loader:
                print(f"[!] Не удалось создать spec для {module_name}.")
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if not hasattr(module, "Information"):
                print(f"[–] {module_name} не содержит класс Information.")
                continue

            if not hasattr(module, "Module"):
                print(f"[–] {module_name} не содержит класс Module.")
                continue

            information_class = module.Information
            module_class = module.Module
            instance = module_class(commands, lumi)

            if hasattr(instance, "_") and callable(instance._):
                instance._()

            loaded_modules.append(instance)
            print(f"[+] Загружен модуль: {getattr(information_class, 'name')} ({getattr(information_class, 'description', 'Нет информации.')}).")
            loaded += 1

        except Exception as e:
            print(f"[!] Ошибка при загрузке модуля {module_name}: {e}.")
            traceback.print_exc()

    print(f"[#] Всего загружено модулей: {loaded}.")
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

# ========================= Imports =========================

import os, \
    sys, \
        asyncio, \
            importlib, \
                re, \
                    requests, \
                            traceback, \
                                subprocess
from pyrogram import Client, \
    filters
from Resources.Misc.anti_spam_block import AntiSpamBlock
from Resources.Misc.milenium import Milenium
from Resources.Luminate.values import _CURRENT, \
    _VERSION, \
        _BUILD, \
            _BRANCH, \
                _FRAMEWORK, \
                    _PREFIX, \
                        _IMAGE_PATH, \
                            _IMAGE_PATH_SMALL, \
                                _API_ID, \
                                    _API_HASH, \
                                            _SESSION, \
                                                _INFO_PATH, \
                                                    custom_commands, \
                                                        system_commands
from Resources.Luminate.loader import loaded_modules, LoadModules

# ========================= Objects =========================

app = Client(_SESSION, _API_ID, _API_HASH)
lumi = AntiSpamBlock(app)

# ========================= Tools =========================

def restart():
    python = sys.executable
    script = os.path.abspath(sys.argv[0])
    args = sys.argv[1:]
    subprocess.Popen([python, script] + args)
    sys.exit()

# ========================= Commands =========================

@app.on_message(filters.command("info", prefixes=_PREFIX) & filters.me)
async def start_command(client, message):
    args = message.text.split()
    with open(_INFO_PATH, "r", encoding="UTF-8") as _INFO:
        _INFO = _INFO.read()
    if '-small' in args:
        await lumi.send_media(message, message.chat.id, _IMAGE_PATH_SMALL, caption=_INFO.format(_VERSION, _BRANCH, _BUILD, _FRAMEWORK, _PREFIX))
    else:
        await lumi.send_media(message, message.chat.id, _IMAGE_PATH, caption=_INFO.format(_VERSION, _BRANCH, _BUILD, _FRAMEWORK, _PREFIX))

@app.on_message(filters.command("help", prefixes=_PREFIX) & filters.me)
async def help_command(client, message):
    help_text = "• Доступные команды:\n"
    for command, description in system_commands.items():
        help_text += f"▣ {command} - {description}\n"

    for command, (handler, description) in custom_commands.items():
        help_text += f"▢ {command} - {description}\n"

    await lumi.send_message(message, message.chat.id, help_text)

@app.on_message(filters.command(["m", "milenium"], prefixes=_PREFIX) & filters.me)
async def milenium_search(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await lumi.send_message(message, message.chat.id, "❌ Укажите запрос.")
        return

    qer = args[1]
    results = Milenium.search(qer)

    if isinstance(results, str):
        await lumi.send_message(message, message.chat.id, results)
        return

    package, info = results[0]

    text = (
        f"📦 `{package}`\n"
        f"👤 Автор: `{info['author']}`\n"
        f"📜 Описание: {info['description']}\n"
        f"🔢 Версия: `{info['version']}`\n"
        f"📂 Файл: `{info['main']}`\n\n"
        f"Лицензия: {info['license']}.\n"
        f"`{_PREFIX}mi {info['main']}`\n"
    )        

    await lumi.send_media(message, message.chat.id, info['placeholder_image'], caption=text)

@app.on_message(filters.command("lm", prefixes=_PREFIX) & filters.me)
async def load_module(client, message):
    if not message.reply_to_message.document or not message.reply_to_message.document.file_name.endswith(".py"):
        await lumi.send_message(message, message.chat.id, f"⚠️ Ответьте на файл .py для загрузки модуля.\nЕсли вы хотите загрузить модуль из ссылки, используйте {_PREFIX}dlm.")
        return

    file_name = message.reply_to_message.document.file_name
    file_path = os.path.join("modules", file_name)

    await lumi.send_message(message, message.chat.id, f"✅ Модуль `{file_name}` загружен.")
    await client.download_media(message.reply_to_message, file_name=file_path)
    restart()

@app.on_message(filters.command("unlm", prefixes=_PREFIX) & filters.me)
async def unload_module(client, message):
    args = message.text.split()
    if len(args) < 2:
        await lumi.send_message(message, message.chat.id, "⚠️ Используйте: ?unlm <имя_модуля>")
        return

    module_name = args[1].strip()
    file_path = os.path.join("modules", f"{module_name}.py")

    if module_name in sys.modules:
        del sys.modules[module_name]

    if os.path.exists(file_path):
        os.remove(file_path)
        await lumi.send_message(message, message.chat.id, f"✅ Модуль `{module_name}` удален.")
        os.execl(sys.executable, sys.executable, f'"{os.path.abspath(sys.argv[0])}"', *sys.argv[1:]) 
    else:
        await lumi.send_message(message, message.chat.id, f"⚠️ Модуль `{module_name}` не найден.")

@app.on_message(filters.command(["dlm", "mi"], prefixes=_PREFIX) & filters.me)
async def download_module(client, message):
    args = message.text.split()
    if len(args) < 2:
        await lumi.send_message(message, message.chat.id, "⚠️ Используйте: ?dlm <ссылка>")
        return

    url = args[1].strip()
    if not url.endswith(".py"):
        await lumi.send_message(message, message.chat.id, "⚠️ Ошибка: Файл должен быть `.py`.")
        return

    file_name = url.split("/")[-1]
    file_path = os.path.join("modules", file_name)

    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        
        spec = importlib.util.spec_from_file_location(file_name[:-3], file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'register_commands'):
            module.register_commands(custom_commands)
            await lumi.send_message(message, message.chat.id, f"✅ Модуль `{file_name}` загружен.")
            os.execl(sys.executable, sys.executable, f'"{os.path.abspath(sys.argv[0])}"', *sys.argv[1:]) 
        else:
            os.remove(file_path)
            await lumi.send_message(message, message.chat.id, "⚠️ Ошибка: В модуле нет `register_commands`.")
    except Exception as e:
        await lumi.send_message(message, message.chat.id, f"❌ Ошибка загрузки: {e}")

@app.on_message(filters.command(["lumi", "l"], prefixes=_PREFIX) & filters.me)
async def check_update_command(client, message):
    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        await lumi.send_message(message, message.chat.id, "❌ Укажите аргументы.")
        return
    
    elif args[1] in ["reload", "rst"]:
        await lumi.send_message(message, message.chat.id, "🔄 Перезагрузка...")
        os.execl(sys.executable, sys.executable, f'"{os.path.abspath(sys.argv[0])}"', *sys.argv[1:]) 
    elif args[1] in ["shutdown", "off"]:
        await lumi.send_message(message, message.chat.id, "🛑 Выключение...")
        os._exit(0)

@app.on_message(filters.text & filters.me)
async def message_handler(client, message):
    match = re.match(f"^{re.escape(_PREFIX)}(\\w+)", message.text)
    if match:
        command = match.group(1)

        if command in custom_commands:
            if message.from_user.id == client.me.id:
                await message.delete()

            try:
                handler, _ = custom_commands[command]
                await handler(message)
            except Exception as e:
                await lumi.send_message(message, message.chat.id, str(e))
                return
        else:
            return

# ========================= Run =========================

def main():
    print("██╗     ██╗   ██╗███╗   ███╗██╗███╗   ██╗ █████╗ ████████╗███████╗\n██║     ██║   ██║████╗ ████║██║████╗  ██║██╔══██╗╚══██╔══╝██╔════╝\n██║     ██║   ██║██╔████╔██║██║██╔██╗ ██║███████║   ██║   █████╗  \n██║     ██║   ██║██║╚██╔╝██║██║██║╚██╗██║██╔══██║   ██║   ██╔══╝  \n███████╗╚██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██║  ██║   ██║   ███████╗\n╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚══════╝")
    LoadModules(custom_commands, lumi)
    print("[#] Юзербот запущен.")
    app.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[#] Остановка...")
    except Exception as e:
        print(f"[#] Ошибка запуска: {e}")

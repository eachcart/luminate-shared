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

import time, random, asyncio, json
from collections import defaultdict, deque
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.raw import functions
from pyrogram.enums import ParseMode

from Resources.Luminate.values import _ASB_SLEEP_MIN, _ASB_SLEEP_MAX

class AntiSpamBlock:
    INVISIBLE_CHARS = ["\u200B", "\u200C", "\u200D", "\u2060"]

    API_LIMITS = {
        "messages.sendMessage": (2, 4),
        "messages.editMessage": (2, 4),
        "messages.deleteMessages": (1, 3),
        "messages.sendMedia": (1, 3),
    }

    def __init__(self, pyro: Client):
        self.pyro = pyro
        self.ratelimit_queue = defaultdict(deque)

    def _sleep(self):
        return random.uniform(_ASB_SLEEP_MIN, _ASB_SLEEP_MAX)

    def _add_invisible_chars(self, text: str) -> str:
        return "".join(c + random.choice(self.INVISIBLE_CHARS) for c in text)

    async def _ratelimit(self, method: str) -> bool:
        now = time.time()
        limit, max_queue = self.API_LIMITS.get(method, (2, 5))
        queue = self.ratelimit_queue[method]

        while queue and now - queue[0] > 1.0:
            queue.popleft()

        if len(queue) >= limit:
            print(f"⛔ Потенциальный спамблок на метод: {method}. Ожидаем...")
            if len(queue) >= max_queue:
                print(f"❌ Запрос отменён во избежание спамблока. ({len(queue)} вызовов за секунду)")
                return False
            await asyncio.sleep(1.5 + self._sleep())
        queue.append(now)
        return True

    async def call(self, method: str, **kwargs):
        if not await self._ratelimit(method):
            return None

        await asyncio.sleep(self._sleep())
        try:
            if method == "messages.sendMessage":
                return await self.pyro.send_message(**kwargs)
            elif method == "messages.editMessage":
                return await self.pyro.edit_message(**kwargs)
            elif method == "messages.sendMedia":
                return await self.pyro.send_photo(**kwargs)
            else:
                raise NotImplementedError(f"Метод {method} не реализован")
        except Exception as e:
            print(f"Ошибка при вызове метода {method}: {e}")
            return None

    #   API 2 Уровня

    async def send_message(self, message, chat_id: int, text: str):
        if message.from_user and message.from_user.id == (await self.pyro.get_me()).id:
            await message.delete()
        return await self.call("messages.sendMessage", chat_id=chat_id, text=text)

    async def edit_message(self, message, chat_id: int, msg_id: int, text: str):
        if message.from_user and message.from_user.id == (await self.pyro.get_me()).id:
            await message.delete()
        return await self.call("messages.editMessage", chat_id=chat_id, msg_id=msg_id, text=text)

    async def send_media(self, message, chat_id: int, media_path: str, caption: str = ""):
        if message.from_user and message.from_user.id == (await self.pyro.get_me()).id:
            await message.delete()
        return await self.call("messages.sendMedia", chat_id=chat_id, photo=media_path, caption=caption)

    async def send_message_via_invoke(self, chat_id: int, text: str):
        try:
            return await self.pyro.invoke(
                functions.messages.SendMessage(
                    peer=chat_id,
                    message=self._add_invisible_chars(text),
                    no_webpage=True,
                    parse_mode="markdown"
                )
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
            return None
class Information:
    name = "Пример"
    description = "Просто пример"

class Module:
    def __init__(self, commands, lumi):
        self.commands = commands
        self.lumi = lumi

    async def example_command(self, message):
        await self.lumi.send_message(message, message.chat.id, "Привет из модуля!")

    def _(self):
        self.commands["example"] = (self.example_command, "Пример команды.")
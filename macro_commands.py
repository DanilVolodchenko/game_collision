from interfaces import ICommand


class MacroCommand:
    def __init__(self, commands: list[ICommand]) -> None:
        self.commands = commands

    def execute(self) -> None:
        for command in self.commands:
            command.execute()

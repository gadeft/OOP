


class CLI:
    def __init__(self, parser, controller) -> None:
        self.parser = parser
        self.controller = controller

    def run(self):
        while True:
            line = input(f"{self.controller.get_current_directory()}:$ ")

            if line == "quit":
                break
            result = None
            try:
                parsed: dict = self.parser.parse(line)
                result = self.controller.run_command(parsed)
            except Exception as e:
                print(e)

            if result is not None:
                print(result)
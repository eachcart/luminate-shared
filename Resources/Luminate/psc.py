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

import re, json

class PSCParser:
    def __init__(self):
        self.data = {}

    def parse(self, text):
        if not text.strip().startswith("#primary-static-config"):
            raise ValueError("Missing #primary-static-config header")

        lines = [line.strip() for line in text.strip().splitlines() if line.strip() and not line.strip().startswith("#")]
        tokens = self._tokenize(lines)
        return self._parse_tokens(tokens)

    def _tokenize(self, lines):
        return lines

    def _parse_tokens(self, tokens):
        stack = [{}]
        keys = []

        for line in tokens:
            if "::" in line:
                key, value = [x.strip() for x in line.split("::", 1)]

                if value == "{":
                    new_obj = {}
                    stack[-1][key] = new_obj
                    stack.append(new_obj)
                    keys.append(key)

                elif value.startswith("[") and value.endswith("]"):
                    stack[-1][key] = json.loads(value)

                elif value.startswith("{") and value.endswith("}"):
                    stack[-1][key] = list(json.loads(value.replace("{", "[").replace("}", "]")))

                elif value == "null":
                    stack[-1][key] = None

                else:
                    try:
                        stack[-1][key] = json.loads(value)
                    except:
                        stack[-1][key] = value.strip('"')

            elif line == "}":
                if len(stack) == 1:
                    raise SyntaxError("Unexpected '}' without opening block")
                stack.pop()
                keys.pop()

            else:
                raise SyntaxError(f"Invalid line (missing '::'): {line}")

        if len(stack) != 1:
            raise SyntaxError("Unclosed block(s) in PSC")

        return stack[0]

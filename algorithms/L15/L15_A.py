ALPHABET = {'nums': '0123456789', 'ops': "+-*/()"}
END_SYMBOL = "."


class Lexer:
    def __init__(self, s):
        self.str = s
        self.i = 0
        self.s_len = len(s)
        self.string_ended = False

    def next_token(self):
        token = ""
        symbol = self.str[self.i]
        if symbol in ALPHABET['ops']:
            token = symbol
        elif symbol == END_SYMBOL:
            self.string_ended = True
        else:
            while symbol in ALPHABET['nums']:
                token += symbol
                self.i += 1
                symbol = self.str[self.i]
            self.i -= 1
        self.i += 1
        return token


my_string = input().strip()
all_tokens = []
lexer = Lexer(my_string)

while not lexer.string_ended:
    token = lexer.next_token()
    all_tokens.append(token)

print("\n".join(all_tokens))

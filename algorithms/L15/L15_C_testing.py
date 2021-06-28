CONSTANTS = {'Ded Moroz': 2020,
             'Moroz': -30,
             'Snegurochka': 10}
FUNCTIONS = ['Podarok(']

ADD, SUB = "+", "-"
MUL, DIV = "*", "/"
LEFT_P, RIGHT_P = "(", ")"
DIGITS = "0123456789"
LETTERS = "DMSPedorznguchka ("
END_SYMBOL = "."

OPS = ADD + SUB + MUL + DIV + LEFT_P + RIGHT_P
ALPHABET = DIGITS + LETTERS + OPS + END_SYMBOL
# Snegurochka+Ded Moroz*Moroz/Moroz+(Podarok(Snegurochka+Ded Moroz)).
# Snegurochka+Ded Moroz*Moroz+Moroz+(Podarok(Snegurochka+Ded Moroz)).


def Podarok(x):
    if x <= 0:
        return -x
    return x + 5


class Lexer:
    def __init__(self, s):
        self.str = s
        self.i = 0
        self.string_ended = False

    def next_token(self):
        current_token = ""
        symbol = self.str[self.i]
        if symbol not in ALPHABET:
            raise ValueError()
        if symbol in OPS:
            current_token = symbol
        elif symbol == END_SYMBOL:
            self.string_ended = True
        elif symbol in DIGITS:
            while symbol in DIGITS:
                current_token += symbol
                self.i += 1
                symbol = self.str[self.i]
            self.i -= 1
        elif symbol in LETTERS:
            while symbol in LETTERS:
                current_token += symbol
                self.i += 1
                symbol = self.str[self.i]
                if self.str[self.i - 1] == LEFT_P:
                    break
            self.i -= 1
            if current_token not in CONSTANTS.keys() and current_token not in FUNCTIONS:
                raise ValueError()

        self.i += 1
        return current_token

    def substitute_constants(self, tokens):
        for i in range(len(tokens)):
            if tokens[i] in CONSTANTS.keys():
                tokens[i] = str(CONSTANTS[tokens[i]])


class Parser:
    def __init__(self):
        self.tokens = None
        self.token_cnt = 0
        self.i = 0

    def parse(self, lexer):
        self.tokens = self.get_tokens(lexer)
        lexer.substitute_constants(self.tokens)
        self.token_cnt = len(self.tokens)
        result = self.evaluate()
        if self.i != self.token_cnt - 1:
            raise ValueError()
        return result

    def get_tokens(self, lexer):
        all_tokens = []
        while not lexer.string_ended:
            token = lexer.next_token()
            all_tokens.append(token)
        return all_tokens

    def evaluate(self):
        first_element = self.term()
        while self.i < self.token_cnt:
            operator = self.tokens[self.i]
            if operator != ADD and operator != SUB:
                break
            else:
                self.i += 1
            second_element = self.term()
            if operator == ADD:
                first_element += second_element
            else:
                first_element -= second_element
        return first_element

    def term(self):
        first_element = self.factor()
        while self.i < self.token_cnt:
            operator = self.tokens[self.i]
            if operator != MUL and operator != DIV:
                break
            else:
                self.i += 1
            second_element = self.factor()
            if operator == MUL:
                first_element *= second_element
            else:
                first_element /= second_element
        return first_element

    def factor(self):
        next_token = self.tokens[self.i]
        if next_token == LEFT_P:
            self.i += 1
            result = self.evaluate()
            if self.i < self.token_cnt:
                expected_bracket = self.tokens[self.i]
            else:
                raise ValueError()
            if self.i < self.token_cnt and expected_bracket == RIGHT_P:
                self.i += 1
                return result
            raise ValueError()

        if next_token == FUNCTIONS[0]:
            self.i += 1
            result = self.evaluate()
            if self.i < self.token_cnt:
                expected_bracket = self.tokens[self.i]
            else:
                raise ValueError()
            if self.i < self.token_cnt and expected_bracket == RIGHT_P:
                self.i += 1
                return Podarok(result)
            raise ValueError()

        self.i += 1
        return int(next_token)


#my_string = input().strip()

fin = open("L13_C_tests.txt")
fout = open("L13_C_answers.txt", 'w')
for my_string in fin.read().splitlines():
    my_string.strip()
    error_exists = False
    ans = 0
    lexer = Lexer(my_string)
    parser = Parser()

    try:
        ans = parser.parse(lexer)
    except ValueError as e:
        error_exists = True

    if error_exists:
        print("WRONG")
        print("WRONG", file=fout)
    else:
        print(ans)
        print(ans, file=fout)

fin.close()
fout.close()

ADD, SUB = "+", "-"
MUL, DIV = "*", "/"
LEFT_P, RIGHT_P = "(", ")"
DIGITS = "0123456789"
END_SYMBOL = "."

OPS = ADD + SUB + MUL + DIV + LEFT_P + RIGHT_P
ALPHABET = DIGITS + OPS + END_SYMBOL


class Lexer:
    def __init__(self, s):
        self.str = s
        self.i = 0
        self.string_ended = False

    def next_token(self):
        if not self.string_ended:
            current_token = ""
            symbol = self.str[self.i]
            if symbol not in ALPHABET:
                raise ValueError()
            if symbol in OPS:
                current_token = symbol
            elif symbol == END_SYMBOL:
                self.string_ended = True
                return None
            else:
                while symbol in DIGITS:
                    current_token += symbol
                    self.i += 1
                    symbol = self.str[self.i]
                self.i -= 1
            self.i += 1
            return current_token
        return None


class Parser:
    def __init__(self):
        self.token = None
        self.lexer = None

    def parse(self, lexer):
        self.lexer = lexer
        result, next_token = self.evaluate(return_bracket=True)
        if next_token is not None:
            raise ValueError()
        return result

    def evaluate(self, return_bracket=False):
        first_element, next_token = self.term(return_operator=True)
        while next_token is not None:
            operator = next_token
            if operator != ADD and operator != SUB:
                break
            second_element, second_operator = self.term(return_operator=True)
            if operator == ADD:
                first_element += second_element
            else:
                first_element -= second_element
            next_token = second_operator
        if return_bracket:
            return first_element, next_token
        return first_element

    def term(self, return_operator=False):
        first_element = self.factor()
        next_token = self.lexer.next_token()
        operator = None
        while next_token is not None:
            operator = next_token
            if operator != MUL and operator != DIV:
                break
            second_element = self.factor()
            if operator == MUL:
                first_element *= second_element
            else:
                first_element /= second_element
            next_token = self.lexer.next_token()
        if return_operator:
            return first_element, next_token
        return first_element

    def factor(self):
        next_token = self.lexer.next_token()
        if next_token == LEFT_P:
            result, expected_bracket = self.evaluate(return_bracket=True)
            if expected_bracket == RIGHT_P:
                return result
            raise ValueError()
        return int(next_token)


my_string = input().strip()

error_exists = False
ans = 0
lexer = Lexer(my_string)
parser = Parser()

try:
    ans = parser.parse(lexer)
except:
    error_exists = True

if error_exists:
    print("WRONG")
else:
    print(ans)

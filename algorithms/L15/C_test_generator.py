from random import randrange, random

CONSTANTS = ['Ded Moroz', 'Moroz', 'Snegurochka']
FUNCTIONS = ['Podarok']
OPERATIONS = ["+", "-", "*"]
LEFT_P, RIGHT_P = "(", ")"
END_SYMBOL = "."

MAX_NUM = 10 ** 3
MAX_OP_CNT = 10
MAX_DEPTH = 5
MESS_UP_PROBA = 0.1
EXPRESSION_CNT = 1000
fout_name = "L13_C_tests.txt"


class Expression:
    def __init__(self, depth=0):
        self.string = ""
        self.depth = depth
        self.add_value()

    def add_value(self):
        value_type = randrange(2)
        if value_type == 0:
            j = randrange(len(CONSTANTS))
            self.string += CONSTANTS[j]
        elif value_type == 1:
            j = randrange(MAX_NUM)
            self.string += str(j)

    def add_operation(self):
        j = randrange(len(OPERATIONS))
        self.string += OPERATIONS[j]
        if self.depth < MAX_DEPTH:
            new_expr = Expression(self.depth + 1)
            expand_expression(new_expr)
            self.string += new_expr.string
        else:
            self.add_value()

    def add_function(self):
        self.string = LEFT_P + self.string + RIGHT_P
        j = randrange(2)
        if j == 0:
            self.string = FUNCTIONS[0] + self.string

    def add_end_symbol(self):
        self.string += END_SYMBOL

    def try_to_mess_up(self):
        p = random()
        if p < MESS_UP_PROBA:
            pass


def expand_expression(expression: Expression):
    op_cnt = randrange(MAX_OP_CNT)
    for i in range(op_cnt):
        op_type = randrange(2)
        if op_type == 0:
            expression.add_operation()
        elif op_type == 1:
            expression.add_function()
    #expression.try_to_mess_up()


fout = open(fout_name, 'w')
for k in range(EXPRESSION_CNT):
    my_expression = Expression()
    expand_expression(my_expression)
    my_expression.add_end_symbol()

    #print(k, len(my_expression.string), "\t\t", my_expression.string)
    print(my_expression.string, file=fout)
fout.close()

import re

NUMBER_PATTERN = '\d+\.*\d*'
OPERATOR_PATTERN = '(\*\*|[+\-*/()])'
PRIORITY_MAP = {'**': 1, '*': 2, '/': 2, '+': 3, '-': 3}

def normalize(expression) :
    replacements = {" " : "", "+-" : "-", "++" : "+", "-+" : "-", "--" : "+"}

    new_expression = "(" + expression + ")"
    for (old, new) in replacements.iteritems():
        new_expression = new_expression.replace(old, new)

    return new_expression


def interpret(expression):
    expression = normalize(expression)
    pos = 0
    operands = []
    operators = []
    last_token = 'a'

    while pos < len(expression):
        token = next_token(expression, pos)
        pos += len(token)

        if last_token == '(' and token == '-':
            operands.append(0)

        if is_number(token):
            operands.append(float(token))

        elif token == '(':
            operators.append(token)

        elif token == ')':
            while operators[-1] != '(':
                shorten_expr(operands, operators)
            operators.pop()

        else:
            while shorten_possible(token, operators):
                shorten_expr(operands, operators)
            operators.append(token)

        last_token = token

    return operands.pop()


def next_token(string, pos):
    number_match = re.match(NUMBER_PATTERN, string[pos:])
    operator_match = re.match(OPERATOR_PATTERN, string[pos:])
    return number_match.group() if number_match else operator_match.group()


def is_number(string):
    return re.match(NUMBER_PATTERN, string) is not None


def shorten_expr(operands, operators):
    b = operands.pop()
    a = operands.pop()
    operator = operators.pop()
    result = None

    if operator == '**':
        result = a ** b
    elif operator == '*':
        result = a * b
    elif operator == '/':
        result = a / b
    elif operator == '+':
        result = a + b
    elif operator == '-':
        result = a - b

    operands.append(result)


def shorten_possible(operator, operators):
    last_operator = operators[-1]
    return last_operator != '(' and PRIORITY_MAP[operator] >= PRIORITY_MAP[last_operator]

while(True):
    expression = raw_input('Please, enter mathematical expression\n')
    print 'result: ' + str(interpret(expression))

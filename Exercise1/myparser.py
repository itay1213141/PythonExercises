from abc import ABC
import re
from numpy import double
from abc import ABC, abstractmethod

number_regex = '^\d+$|^\d+\.\d+$'
prec = {'-u': 5, '*': 4, '/': 3, '+': 1, '-': 1, '(': 0, '': 9}
unary = ['-u']


def get_precedence(op):
    return prec.get(op, -1)


class Expression(ABC):
    @abstractmethod
    def calc(self) -> double:
        pass


class Num(Expression):
    def __init__(self, number) -> None:
        self.number = number

    def calc(self) -> double:
        return self.number

    def __str__(self) -> str:
        return str(self.number)

class UnaryMinus(Expression):
    def __init__(self, expression) -> None:
        self.expression = expression

    def calc(self) -> double:
        return -self.expression.calc()

    def __str__(self) -> str:
        return f'(-{str(self.expression)})'

class BinExp(Expression):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right


class Plus(BinExp):
    def __init__(self, left, right) -> None:
        super().__init__(left, right)

    def calc(self) -> double:
        return self.left.calc() + self.right.calc()

    def __str__(self) -> str:
        return f'{str(self.left)}+{str(self.right)}'

class Minus(BinExp):
    def __init__(self, left, right) -> None:
        super().__init__(left, right)

    def calc(self) -> double:
        return self.left.calc() - self.right.calc()

    def __str__(self) -> str:
        return f'{str(self.left)}-{str(self.right)}'

class Mul(BinExp):
    def __init__(self, left, right) -> None:
        super().__init__(left, right)

    def calc(self) -> double:
        return self.left.calc() * self.right.calc()

    def __str__(self) -> str:
        return f'{str(self.left)}*{str(self.right)}'

class Div(BinExp):
    def __init__(self, left, right) -> None:
        super().__init__(left, right)

    def calc(self) -> double:
        return self.left.calc() / self.right.calc()

    def __str__(self) -> str:
        return f'{str(self.left)}/{str(self.right)}'

def split_tokens(expression):
    tokens = re.split('([+\-*/()]|\d+\.\d+|\d+)', expression.strip())

    operators_stack = []
    queue = []
    last = ''

    for token in tokens:
        if not token:
            continue

        if token == '-' and get_precedence(last) >= 0:
            token = '-u'

        # If its a number
        if re.match(number_regex, token):
            # If it follows another number or a close parentheses
            if re.match(number_regex, last) or last == ')':
                raise Exception("Value tokens must be separated by an operator")

            queue.append(token)
        elif token == '(':
            operators_stack.append(token)
        elif token == ')':
            while operators_stack[-1] != '(':
                operator = operators_stack.pop()
                queue.append(operator)

            if operators_stack.pop() != '(':
                raise Exception("No matching (")
        elif get_precedence(token) > 0:
            precedence = get_precedence(token)
            
            if token in unary:
                while operators_stack and precedence < get_precedence(operators_stack[-1]):
                    queue.append(operators_stack.pop())
            else:
                while operators_stack and precedence <= get_precedence(operators_stack[-1]):
                    queue.append(operators_stack.pop())

            operators_stack.append(token)
        else:
            raise Exception(f"Unknown token: {token}")

        last = token

    while operators_stack:
        queue.append(operators_stack.pop())

    return queue
               
            
def parser(expression: str) -> float:
    tokens = split_tokens(expression)
    stack = []
    
    for token in tokens:
        if token in '+-*/':
            right = stack.pop()
            left = stack.pop()
            
            if token == '+':
                stack.append(Plus(left, right))
            elif token == '-':
                stack.append(Minus(left, right))
            elif token == '*':
                stack.append(Mul(left, right))
            elif token == '/':
                stack.append(Div(left, right))
        elif token == '-u':
            stack.append(UnaryMinus(stack.pop()))
        else:
            stack.append(Num(float(token)))
    
    return stack[0].calc()

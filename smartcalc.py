import re


class SmartCalc:
    def __init__(self):
        self.var_dict = {}
        self.operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: b - a,
            '/': lambda a, b: b / a,
            '*': lambda a, b: a * b,
            '^': lambda a, b: b ** a}
        self.errors = {1: 'Unknown command',
                       2: 'Invalid identifier',
                       3: 'Invalid assignment',
                       4: 'Invalid expression',
                       5: 'Unknown variable',
                       6: 'Zero division error'}
        self.order = {')': 0, '(': 0, '+': 1, '-': 1, '/': 2, '*': 2, '^': 3}
        self.exp_arr = []

    def start(self):
        expression = input()
        while expression != '/exit':
            if expression == '/help':
                print(f'SmartCalc app can handle {list(self.operators.keys())} operators')
            elif expression and expression[0] == '/':
                print(self.errors[1])
            elif '=' in expression:
                self.assignment_handler(expression)
            elif expression and expression != '\t':
                result, error = self.expression_handler(expression)
                if result is False:
                    print(error)
                else:
                    print(result)
            expression = input()
        print('Bye!')

    def assignment_handler(self, exp):
        key, val = exp.split('=', 1)
        key = key.strip()
        check, error = self.check_assignment(key, val)
        if check:
            result, error = self.expression_handler(val)
            if result is False:
                print(error)
            else:
                self.var_dict[key] = str(result)
        else:
            print(error)

    def check_assignment(self, key, val):
        if not key.isalpha():
            return False, self.errors[2]
        if '=' in val:
            return False, self.errors[3]
        return True, None

    def expression_handler(self, exp):
        exp = exp.replace(' ', '')
        self.exp_arr = [i for i in re.split(r'([+-]+|[/*()^ ])', exp) if i != '' and i != ' ']
        check, error = self.check_expression()
        if not check:
            return False, error
        result, error = self.infix_to_postfix()
        if not result:
            return False, error
        result, error = self.calc_expression(result)
        if result is False:
            return False, error
        return result, None

    def check_expression(self):
        for i, el in enumerate(self.exp_arr):
            if el.isalnum() and not el.isalpha() and not el.isdigit():
                return False, self.errors[4]
            elif el.isalpha():
                if el not in self.var_dict:
                    return False, self.errors[5]
                self.exp_arr[i] = self.var_dict[el]
            elif '+' in el or '-' in el:
                self.exp_arr[i] = '+' if len(el) % 2 == 0 or '+' in el else '-'
                if i == 0 or self.exp_arr[i - 1] == '(':
                    self.exp_arr.insert(i, '0')
                    continue
        return True, None

    def infix_to_postfix(self):
        postfix_stack = []
        operators_stack = []
        for el in self.exp_arr:
            if el not in self.order:
                postfix_stack.append(el)
            elif el == '(':
                operators_stack.append(el)
            elif el == ')':
                if '(' not in operators_stack:
                    return False, self.errors[4]
                while operators_stack[-1] != '(':
                    postfix_stack.append(operators_stack.pop())
                operators_stack.pop()
            elif el in self.operators:
                while operators_stack and self.order[el] <= self.order[operators_stack[-1]]:
                    postfix_stack.append(operators_stack.pop())
                operators_stack.append(el)

        if '(' in operators_stack:
            return False, self.errors[4]
        while operators_stack:
            postfix_stack.append(operators_stack.pop())
        return postfix_stack, None

    def calc_expression(self, post_exp):
        res_stack = []
        for el in post_exp:
            if el in self.operators:
                if len(res_stack) < 2:
                    return False, self.errors[4]
                a, b = int(res_stack.pop()), int(res_stack.pop())
                if a == 0 and el == '/':
                    return False, self.errors[6]
                res = self.operators[el](a, b)
                res_stack.append(int(res))
            else:
                res_stack.append(int(el))
        if len(res_stack) > 1:
            return False, self.errors[4]
        return res_stack[0], None


app = SmartCalc()
app.start()

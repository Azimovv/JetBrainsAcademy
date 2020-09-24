from collections import deque

variable_dict = {}
operations = ['+', '-', '*', '/']


def is_number(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def make_readable(operation):
    op_clean = operation.replace(' ', '')
    readable_list = []
    minus_count = 0

    for x in range(len(op_clean)):
        if x > 0 and op_clean[x] not in operations:
            if is_number(op_clean[x - 1]) and is_number(op_clean[x]):
                readable_list.append(str((int(op_clean[x - 1]) * 10) + int(op_clean[x])))
                readable_list.pop(-2)
            elif op_clean[x - 1] == '-' and minus_count > 0:
                if minus_count % 2 == 1:
                    readable_list.append('-')
                else:
                    readable_list.append('+')
                readable_list.append(op_clean[x])
                minus_count = 0
            else:
                readable_list.append(op_clean[x])
        else:
            if op_clean[x] == '+':
                if op_clean[x - 1] != '+':
                    readable_list.append(op_clean[x])
            elif op_clean[x] == '*':
                if op_clean[x - 1] != '*':
                    readable_list.append(op_clean[x])
                else:
                    return 'Invalid expression'
            elif op_clean[x] == '/':
                if op_clean[x - 1] != '/':
                    readable_list.append(op_clean[x])
                else:
                    return 'Invalid expression'
            elif op_clean[x] == '-':
                minus_count += 1
            else:
                readable_list.append(op_clean[x])

    return readable_list


def postfix_conv(operation):
    precedence = {'*': 3,
                  '/': 3,
                  '+': 2,
                  '-': 2,
                  '(': 1}
    postfix = []
    stack = deque()
    try:
        for i in operation:
            if i.isalpha() or is_number(i):
                postfix.append(i)
            elif i == '(':
                stack.append(i)
            elif i == ')':
                top = stack.pop()
                while top != '(':
                    postfix.append(top)
                    top = stack.pop()
            else:
                while len(stack) != 0 and \
                        (precedence[stack[-1]] >= precedence[i]):
                    postfix.append(stack.pop())
                stack.append(i)
        while len(stack) != 0:
            postfix.append(stack.pop())
    except IndexError:
        return 'Invalid expression'
    else:
        return postfix


def variable_assignment(assignment_input):
    assign_list = assignment_input.replace(' ', '').split('=')
    if not assign_list[0].isalpha():
        print('Invalid identifier')
    else:
        if len(assign_list) > 2:
            print('Invalid assignment')
        elif is_number(assign_list[1]):
            variable_dict[assign_list[0]] = int(assign_list[1])
        elif assign_list[1].isalpha():
            if assign_list[1] in variable_dict.keys():
                variable_dict[assign_list[0]] = variable_dict[assign_list[1]]
            else:
                print('Unknown variable')
        else:
            print('Invalid assignment')


def do_calc(postfix_eq):
    operands = deque()

    try:
        for i in postfix_eq:
            if is_number(i):
                operands.append(int(i))
            elif i.isalpha():
                operands.append(variable_dict[i])
            else:
                op2 = operands.pop()
                op1 = operands.pop()
                if i == '*':
                    operands.append(op1 * op2)
                elif i == '/':
                    operands.append(op1 // op2)
                elif i == '+':
                    operands.append(op1 + op2)
                elif i == '-':
                    operands.append(op1 - op2)
                else:
                    return 'Invalid expression'
    except (IndexError, KeyError):
        return 'Invalid expression'
    else:
        return operands.pop()


while True:
    nums = input()
    if nums.startswith('/'):
        if nums.endswith('exit'):
            print('Bye!')
            break
        elif nums.endswith('help'):
            print('The program calculates the sum of numbers, + is addition, - is subtraction')
        else:
            print('Unknown command')
    elif nums == '':
        continue
    elif is_number(nums):
        print(nums)
    elif nums.strip().isalpha() and '=' not in nums:
        if nums in variable_dict.keys():
            print(variable_dict[nums])
        else:
            print('Unknown variable')
    else:
        if '=' in nums:
            variable_assignment(nums)
        else:
            new_op = postfix_conv(make_readable(nums))
            print(do_calc(new_op))

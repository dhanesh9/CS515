import sys

# define supported operators
operators = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "^": "EXPO", "%": "MOD"}

# initializing global variable map
global_vars = {}
print_flag = False

def parse_expression(expression):
    # Tokenize the input expression
    tokens = []
    current_token = ""
    prev_operator = False
    operator_flag = True
    # print(f"Received expression as :- {expression}")
    my_list = expression.split(" ")
    # print(f"received mylist as :- {my_list}")
    variables_to_assign = []
    for loop_token in my_list:
        # print(f"Current loop token is :- {loop_token}")
        if loop_token == "":
            continue
        if loop_token == "print":
            global print_flag
            print_flag = True
            if my_list.index("print") != 0:
                raise ValueError(f"parse error")

            new_string = expression
            print_str = new_string.replace("print", "", 1)
            print_str.strip()
            # print(f"Now : {print_str}")
            final_str = print_str.split(",")
            final_str = [string.strip() for string in final_str]

            # Checking for invalid spaces.
            for temp_char in final_str:
                temp_char = temp_char.replace(" ", "")
                if " " in temp_char:
                    raise ValueError(f"parse error")

            # Collecting valid variables/expressions for printing.
            final_str = [x for x in final_str if x != ""]
            # print(final_str)
            tokens.append("print")

            tokens.extend([element for element in final_str])
            # operators = ["+", "-", "*", "/", "^", "(", ")", "="]
            equality = ["="]

            for element in final_str:
                if any(char in element for char in equality):
                    raise ValueError(f"parse error")

            # Block for handling expressions in print statement.
            # print(f"Final STR before block is :- {final_str}")
            for element in final_str:
                if any(char in element for char in operators):
                    # print(f"'{element}' contains a special character")
                    ind = final_str.index(element)
                    # print(f"Final str is : {final_str}")
                    # print(f"The index is :- {ind}")
                    temp = "" + final_str[ind]
                    p_exp, var_temp = parse_expression(temp)
                    res = evaluate_expression(p_exp)
                    ind = tokens.index(element)
                    tokens[ind] = str(res)
                    # print(f"Final_str is :- {final_str}")
            # print(f"final tokens in print are : {tokens}")
            output, variables_to_assign = tokenize(tokens)
            return output, variables_to_assign

        elif '=' in loop_token and 0 < loop_token.index('=') < (len(loop_token) - 1):
            # If '=' is in the current token, split it and add '=' as a separate token
            split_token = loop_token.split("=")
            split_token[0].strip()
            split_token[1].strip()
            if len(split_token) != 2 or not split_token[0].isalnum():
                raise ValueError(f"parse error")
            # Appending the variable name to the list of variables to assign
            # variables_to_assign.append(split_token[0])
            # Append the split tokens to the list of tokens
            tokens.append(split_token[0])
            tokens.append("=")
            # tokens.append(split_token[1])
            loop_token = split_token[1]
            for char in loop_token:
                # print(f"Current char is :- {char}")
                if char == "":
                    continue
                if char.isalnum():
                    if operator_flag:
                        current_token += char
                        prev_operator = False
                    else:
                        raise ValueError(f"parse error")
                else:
                    if current_token != "":
                        tokens.append(current_token)
                        current_token = ""
                    if char in ["+", "-", "*", "/", "^", "(", ")", "=", "%"]:
                        tokens.append(char)
                        operator_flag = True
                        prev_operator = True
                    else:
                        raise ValueError(f"parse error")

            prev_operator = True
            operator_flag = True
            # print(f"In 2nd case current_token is : {current_token}")

        else:
            # print(f"In last case entering current_token is : {current_token}")
            for char in loop_token:
                # print(f"Current char is :- {char}")
                if char == "":
                    continue
                if char == ".":
                    current_token += char
                    # print(current_token)
                    prev_operator = False
                    continue

                if char.isalnum():
                    if operator_flag:
                        current_token += char
                        prev_operator = False
                    else:
                        raise ValueError(f"parse error")
                else:
                    if current_token != "":
                        tokens.append(current_token)
                        current_token = ""
                    if char in ["+", "-", "*", "/", "^", "(", ")", "=", "%"]:
                        tokens.append(char)
                        operator_flag = True
                        prev_operator = True
                    else:
                        raise ValueError(f"parse error")

            if not prev_operator:
                operator_flag = False
            # print(f"In last case current_token is : {current_token}")

    # print(f"current_token is : {current_token}")
    if current_token != "":
        tokens.append(current_token)

    # print(f"final tokens are : {tokens}")
    output, variables_to_assign = tokenize(tokens)
    return output, variables_to_assign


def tokenize(tokens):
    # print(f"Received tokens as : {tokens}")
    # Parse the tokens
    output = []
    operator_stack = []
    variables_to_assign = []
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
    for i, token in enumerate(tokens):
        # print(f"Current token value is :- {token}")
        # Storing the next element
        if i < len(tokens) - 1:
            next_element = tokens[i + 1]
            if next_element == "=":
                variables_to_assign.append(token)

        else:
            next_element = None

        if token.isnumeric():
            output.append(("NUMBER", float(token)))
        elif token == "print":
            global print_flag
            print_flag = True
            output.append(("KEYWORD", token))
        elif token.isalnum():
            output.append(("VARIABLE", token))
        elif token in ["+", "-", "*", "/", "%"]:
            while operator_stack and operator_stack[-1] != "(" and precedence[operator_stack[-1]] >= precedence[token]:
                output.append(("OPERATOR", operator_stack.pop()))
            operator_stack.append(token)
        elif token == "^":
            while operator_stack and operator_stack[-1] != "(" and precedence[operator_stack[-1]] >= precedence[token]:
                output.append(("OPERATOR", operator_stack.pop()))
            operator_stack.append(token)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                output.append(("OPERATOR", operator_stack.pop()))
            if not operator_stack:
                raise ValueError(f"parse error")
            operator_stack.pop()
        elif token == "=":
            while operator_stack:
                output.append(("ASSIGNMENT_OPERATOR", operator_stack.pop()))
            output.append(("OPERATOR", token))
        elif "." in token:
            output.append(("NUMBER", float(token)))
        elif token == "divide by zero":
            output.append(("ERROR", token))
        else:
            raise ValueError(f"parse error")

    while operator_stack:
        if operator_stack[-1] == "(":
            raise ValueError(f"parse error")
        output.append(("OPERATOR", operator_stack.pop()))

    return output, variables_to_assign


#########################################################################

def evaluate_expression(parsed_expression):
    # print(f"in Evaluator Func Received parsed_expression as : {parsed_expression}")
    stack = []
    var_name = ""
    flag = False
    for i, token in enumerate(parsed_expression):
        token_type, token_value = token
        # print(f"Token type is : {token_type}. And token value is : {token_value}")
        if token_type == 'NUMBER':
            stack.append(float(token_value))
        elif token_type == 'VARIABLE':

            if i + 1 < len(parsed_expression) and token_value not in global_vars and parsed_expression[i + 1][1] == "=":
                # if token_value not in global_vars and parsed_expression[i + 1][1] == "=":
                # print(f"Inside condition.......................................................................")
                global_vars[token_value] = float(0)
                var_name = token_value

            elif i + 1 < len(parsed_expression) and token_value in global_vars and parsed_expression[i + 1][1] == "=":
                var_name = token_value

            elif token_value in global_vars:
                # print(f"Token type is : {token_type}. And token value is : {token_value}")
                stack.append(float(global_vars[token_value]))
            else:
                raise ValueError(f"parse error")

        elif token_type == 'OPERATOR' and token_value == "=":
            flag = True
            continue

        elif token_type == 'OPERATOR' and token_value != "=":
            if token_value in operators:
                # print(f"Token type is : {token_type}. And token value is : {token_value}")
                # print(f"stack is : {stack}")
                if len(stack) < 2 and token_value == "-":
                    # print("In now")
                    temp = stack.pop()
                    # print(f"stack is : {stack}")
                    stack.append(float(temp))
                    stack.append(float(temp * 2))
                    # print(f"stack is : {stack}")
                    # test
                if len(stack) < 2:
                    raise ValueError(f"parse error")
                # print(f"here Stack is : {stack}")

                if token_value != "^":
                    operand2 = stack.pop()
                    operand1 = stack.pop()
                result = 0.0
                # Code for each operator to be coded
                if token_value == "-":
                    result = float(operand1 - operand2)

                elif token_value == "+":
                    result = float(operand1 + operand2)

                elif token_value == "*":
                    result = float(operand1 * operand2)

                elif token_value == "/":
                    # print(f"op1 is {operand1} ...... op2 is {operand2} ... res is {result}")
                    if float(operand2) == 0.0 :
                        result = "divide by zero"
                        # raise ValueError(f"divide by zero")
                        # print(f"op1 is {operand1} ...... op2 is {operand2} ... res is {result}")
                        # print(f"print flag is {print_flag}")
                        if not print_flag:
                            # print("I am here finally")
                            print(result)

                    else:
                        result = float(operand1 / operand2)

                elif token_value == "%":
                    result = float(operand1 % operand2)

                elif token_value == "^":
                    t_flag = False
                    multiple = False
                    x = i
                    result = 1.0
                    for j,temp in enumerate(parsed_expression):
                        if t_flag:
                            t_flag = False
                            continue
                        if(i > j):
                            continue
                        if j < (len(parsed_expression) - 2) and parsed_expression[j+1][0] == "NUMBER" and parsed_expression[j+2][1] == "^":
                            t_flag = True
                            multiple = True
                            continue
                        # print(f"Current val is {parsed_expression[j]}")
                        # print(f"Current loop val is {j}")
                        break

                    if multiple:
                        # print("In multiple ")
                        # print(f"Value of i is :- {i}")
                        while(j >= i):
                            # print(f"Value of j is :- {j}")
                            if parsed_expression[j][1] == "^":
                                del (parsed_expression[j])
                                j = j-1
                                pow_operand = float(parsed_expression[j][1])
                                # print(f"pow_operand is {pow_operand}")
                                last_opr = float(parsed_expression[j][1])
                                del (parsed_expression[j])
                                # print(f"Now parsed_expression is : {parsed_expression}")
                                j = j-1
                                result = pow(pow_operand, result)
                            else:
                                j = j-1
                                # print(f"Now result is {result}")
                                # print(f"Now parsed_expression is : {parsed_expression}")

                        # print(f"After loop Value of j is :- {j}")
                        # print(f"pow_operand is {pow_operand}")
                        pow_operand = float(parsed_expression[j][1])
                        # print(f"After loop pow_operand is {pow_operand}")
                        del (parsed_expression[j])
                        result = pow(pow_operand, result)
                        parsed_expression.insert(j, ('NUMBER', result))
                        # print(f"Finally result is {result}")
                        # print(f"Finally parsed_expression is : {parsed_expression}")

                        res = evaluate_expression(parsed_expression)
                        return(res)

                    else:
                        operand2 = stack.pop()
                        operand1 = stack.pop()
                        result = pow(operand1, operand2)
                        # print(f"Test Print ::-- op1 is {operand1} op2 is {operand2} result is {result}")

                # result = operators[token_value](operand1, operand2)
                stack.append(result)
                # print(f"length of stack is : - {len(stack)}")
                # print(f"Stack is : {stack}")
            else:
                raise ValueError(f"parse error")

        elif token_type == "KEYWORD" and token_value == "print":
            # print_flag = True
            # print(f"In print.....Global vars is ... {global_vars}")
            # print(f"---------------------------------------------------------------Stack value is :- {stack}")
            for x in range(1, len(parsed_expression)):
                if parsed_expression[x][0] == "NUMBER":
                    val = parsed_expression[x][1]
                    # print(f".Num val now is {val}")
                elif parsed_expression[x][0] == "ERROR":
                    val = "divide by zero"
                    # print(f".val now is {val}")
                else:
                    val = global_vars[parsed_expression[x][1]]
                    # print(f".val now is {val}")
                stack.append(val)
                # print(f"Stack now is :- {stack}")

            # print(f"---------------------------------------------------------------Stack value is :- {stack}")
            print(" ".join(str(x) for x in stack))
            return 0

        else:
            raise ValueError(f"parse error")

    if len(stack) == 1:
        result = stack.pop()
        if flag: global_vars[var_name] = result
        return result
    else:
        raise ValueError(f"parse error")


#######################################################################


def remove_multi_comments(string):
    result = ""
    i = 0
    while i < len(string):
        if string[i:i + 2] == "/*":
            i += 2
            while i < len(string) and string[i:i + 2] != "*/":
                i += 1
            i += 2
        elif string[i:i + 2] == "//":
            i += 2
            while i < len(string) and string[i] != "\n":
                i += 1
        else:
            result += string[i]
            i += 1
    return result


def main():
    try:
        # expression = input('Enter an expression to parse: ').strip()
        expression = sys.stdin.read()
        expression = remove_multi_comments(expression)
        line_expression = expression.split("\n")
        while "" in line_expression:
            line_expression.remove("")
        # print(line_expression)
        # line_expression = """x  = 3
        # y  = 5
        # z  = 2 + x * y
        # z2 = (2 + x) * y
        # m = 25
        # n = m % 10
        # print x, y, z, z2,m,n"""
        # line_expression = """pi = 3.14159
        # r = 2
        # area = pi * r^2
        # print area"""
        # line_expression = line_expression.split("\n")
        for exp in line_expression:
            exp = exp.strip()
            if exp == "" or exp.startswith("#"):
                continue
            # print(f"Sending expression now: {exp}")
            parsed_exp, test_var = parse_expression(exp)
            # print(f'Parsed expression: {parsed_exp}')
            # print(f'Variable for assignment: {test_var}')

            result = evaluate_expression(parsed_exp)
            # print(f"result is : - {result}")
            # print(f"vars : ... - {global_vars}")

    except Exception as e:
        print(f'{e}')


if __name__ == '__main__':
    main()

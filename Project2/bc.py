def evaluate_expression(expr, variables):
    # Replace variable names with their values in the expression
    for var, val in variables.items():
        expr = expr.replace(var, str(val))

    expr = expr.replace('^', '**')
    # Evaluate the expression using Python's eval function
    result = eval(expr)
    return result

def parse_input(s, variables):
    if '=' in s:
        var, val = s.split('=')
        var = var.strip()
        val = evaluate_expression(val, variables)
        variables[var] = val
    else:
        stack = []
        num, sign = 0, "+"
        for i, char in enumerate(s):
            if char.isdigit():
                num = num * 10 + int(char)
            elif char.isalpha():
                var_name = char
                j = i + 1
                while j < len(s) and s[j].isalnum():
                    var_name += s[j]
                    j += 1
                if var_name in variables:
                    num = variables[var_name]
                    i = j - 1
                else:
                    print(f"Error: Undefined variable '{var_name}'")
                    return None
            elif char in "+-*/":
                if sign == "+":
                    stack.append(num)
                elif sign == "-":
                    stack.append(-num)
                elif sign == "*":
                    stack.append(stack.pop() * num)
                elif sign == "/":
                    stack.append(int(stack.pop() / num))
                num, sign = 0, char
            elif char == "(":
                subexpr = s[i+1:]
                j = 0
                while j < len(subexpr):
                    if subexpr[j] == "(":
                        stack.append("(")
                    elif subexpr[j] == ")":
                        if isinstance(stack[-1], int):
                            b = stack.pop()
                            op = stack.pop()
                            a = stack.pop()
                            stack.append(eval(f"{a} {op} {b}"))
                        else:
                            stack.pop()
                            break
                    j += 1
                i += j + 1
        if sign == "+":
            stack.append(num)
        elif sign == "-":
            stack.append(-num)
        elif sign == "*":
            stack.append(stack.pop() * num)
        elif sign == "/":
            stack.append(int(stack.pop() / num))
        while len(stack) > 1:
            b = stack.pop()
            op = stack.pop()
            a = stack.pop()
            stack.append(eval(f"{a} {op} {b}"))
        result = stack.pop()
        print(result)

variables = {}
while True:
    user_input = input(" ")
    if user_input.lower() == "quit":
        break
    parse_input(user_input, variables)



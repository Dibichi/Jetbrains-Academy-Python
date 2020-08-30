def command_handler():
    global user_calc
    if user_calc == '/exit':
        print("Bye!")
        exit()

    elif user_calc == '/help':
        print('The program calculates the sum of numbers')

    else:
        print('Unknown command')


def assignment(user):
    no_spaces = user_calc.replace(' ', '').split('=')
    if no_spaces[0].isalpha() is False:
        print('Invalid identifier')

    elif ((no_spaces[-1].isalpha() is False) and (no_spaces[-1].isdigit() is False)) or len(no_spaces) > 2:
        print('Invalid assignment')

    else:
        if no_spaces[-1] in the_variables:
            the_variables[no_spaces[0]] = the_variables[no_spaces[-1]]

        elif no_spaces[-1].isdigit():
            the_variables[no_spaces[0]] = no_spaces[-1]

        else:
            print('Unknown variable')


def expression_separator(user):
    no_expressions = user
    for remove in ['+', '-', '=', '*', '/', '(', ')']:
        no_expressions = no_expressions.replace(remove, ' ')

    return no_expressions.split()


def do_math(expression):
    if '//' in expression:
        return print("Invalid expression")

    try:
        print(int(eval(expression)))
    except:
        print('Invalid Expression')


the_variables = {}

while True:
    user_calc = input()
    variables = expression_separator(user_calc)

    # Takes care of all / commands
    if user_calc.startswith('/'):
        command_handler()

    # Handles single expressions
    elif len(variables) == 1:
        if variables[0].isalpha():
            print(the_variables.setdefault(user_calc, "Unknown variable"))

        elif variables[0].isdigit():
            do_math(user_calc)

        else:
            print('Invalid identifier')

    # Negates blank inputs, handles variables, and handles expressions
    elif len(variables) > 1:

        # Checks for assigning variables
        if '=' in user_calc:
            assignment(user_calc)

        # Actual math operations
        else:
            if all(map(lambda v: v.isdigit(), variables)):
                do_math(user_calc)

            elif all(map(lambda v: v.isalpha() or v.isdigit(), variables)):
                user_calc = user_calc.split()
                for var in range(len(user_calc)):
                    if user_calc[var].isalpha():
                        user_calc[var] = the_variables[user_calc[var]]

                user_calc = ' '.join(user_calc)
                do_math(user_calc)


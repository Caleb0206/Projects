from stack_array import Stack

# You do not need to change this class
class PostfixFormatException(Exception):
    pass


def helper_try_cast(value):
    ''' A helper function to try casting a string, precondition: number, into an int or a float'''
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            raise PostfixFormatException("Invalid token")
    return value

def postfix_eval(input_str):
    '''Evaluates a postfix expression

    Input argument:  a string containing a postfix expression where tokens
    are space separated.  Tokens are either operators + - * / ** >> << or numbers.
    Returns the result of the expression evaluation.
    Raises an PostfixFormatException if the input is not well-formed
    DO NOT USE PYTHON'S EVAL FUNCTION!!!'''

    if input_str == '':
        raise PostfixFormatException("Empty input")
    rpn = Stack(30)
    # check amount of operators and operands
    operator = 0
    operand = 0
    for thing in input_str.split(' '):
        if thing != ' ' and thing != '':
            if thing == '<<' or thing == '>>' or thing == '**' or thing == '*' or thing == '/' or thing == '+' or thing == '-':
                operator += 1
            else:
                # see if it is a valid operand or not (will raise Invalid token error if it is not)
                helper_try_cast(str(thing))
                operand += 1
    # if there are more operators than numbers, insufficient operands
    if operand <= operator:
        raise PostfixFormatException("Insufficient operands")
    elif operand > operator + 1:
        # more numbers than operators, too many operands
        raise PostfixFormatException("Too many operands")

    # if there are good amount of operands and operators, proceed normally
    for thing in input_str.split(' '):
        if thing != ' ' and thing != '':
            if thing != '<<' and thing != '>>' and thing != '**' and thing != '*' and thing != '/' and thing != '+' and thing != '-':
                rpn.push(str(thing))
            else:
                if thing == '<<' or thing == '>>':
                    a = str(rpn.pop())
                    b = str(rpn.pop())
                    try:
                        if thing == '<<':
                            result = int(b) << int(a)
                            rpn.push(result)
                        else:
                            result = int(b) >> int(a)
                            rpn.push(result)
                    except ValueError:
                        raise PostfixFormatException("Illegal bit shift operand")
                elif thing == "**":
                    a = helper_try_cast(str(rpn.pop()))
                    b = helper_try_cast(str(rpn.pop()))
                    rpn.push(b**a)
                elif thing == "*" or thing == "/":
                    a = helper_try_cast(str(rpn.pop()))
                    b = helper_try_cast(str(rpn.pop()))
                    if thing == '*':
                        rpn.push(b * a)
                    else:
                        if a == 0:
                            raise ValueError
                        rpn.push(b / a)
                elif thing == "+" or thing == "-":
                    a = helper_try_cast(str(rpn.pop()))
                    b = helper_try_cast(str(rpn.pop()))
                    if thing == '+':
                        rpn.push(b + a)
                    else:
                        rpn.push(b - a)
    return helper_try_cast(str(rpn.pop()))

def infix_to_postfix(input_str):
    '''Converts an infix expression to an equivalent postfix expression

    Input argument:  a string containing an infix expression where tokens are
    space separated.  Tokens are either operators + - * / ** >> << parentheses ( ) or numbers
    Returns a String containing a postfix expression '''
    rpn = ""
    operator = Stack(30)

    for thing in input_str.split():
        if thing != '(' and thing != ')' and thing != '<<' and thing != '>>' and thing != '**' and thing != '*' and thing != '/' and thing != '+' and thing != '-':
            rpn += thing + " " # add to string output if it is just a number
        elif thing == '(':
            operator.push(thing)
        elif thing == ')':
            while operator.peek() != '(':
                rpn += operator.pop() + " "
            operator.pop() #pops the '(' without adding it to the RPN string
        elif thing == '<<' or thing == '>>':
            operator.push(thing)
        elif thing == '**':
            ## << and >> has greater presedence than **
            if operator.size() > 0 and (operator.peek() == '<<' or operator.peek() == '>>'):
                rpn += operator.pop() + " "
            operator.push('**')
        elif thing == '*' or thing == '/':
            # first value of stack has same or greater precedence, pop
            while operator.size() > 0 and (operator.peek() == '**' or operator.peek() == "*" or operator.peek() == '/' or operator.peek() == '<<' or operator.peek() == '>>'):
                rpn += operator.pop() + " "
            # if paren is False:
            operator.push(thing)
        elif thing == '+' or thing == '-':
            # first value of stack has same or greater precedence, pop
            while operator.size() > 0 and (operator.peek() == '**' or operator.peek() == "*" or operator.peek() == '/' or operator.peek() == '+' or operator.peek() == '-'
                     or operator.peek() == '<<' or operator.peek() == '>>'):
                rpn += operator.pop() + " "
            # if paren is False:
            operator.push(thing)
    # pop the rest of the operators until Stack is empty
    while operator.size() > 0:
        rpn += operator.pop() + " "
    # remove the extra space at the end
    return rpn.strip()

def prefix_to_postfix(input_str):
    '''Converts a prefix expression to an equivalent postfix expression

    Input argument:  a string containing a prefix expression where tokens are
    space separated.  Tokens are either operators + - * / ** >> << or numbers
    Returns a String containing a postfix expression (tokens are space separated)'''

    expression = Stack(30)
    # no parentheses check needed
    for string in reversed(input_str.split()):
        if string != ' ' or '':
            if string != '<<' and string != '>>' and string != '**' and string != '*' and string != '/' and string != '+' and string != '-':
                expression.push(string) # if it is a number, push number to stack
            else:
                # pop numbers if encountered an operator
                temp = expression.pop() + " " + expression.pop() + " " + string
                expression.push(temp)
    return expression.pop().strip() # get rid of extra spaces


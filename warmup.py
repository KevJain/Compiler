# warmup.py
#
# Lewis, suffering through the hardship of his Algebra 2 class, has
# decided to write a computer program to help him with his homework.
# His thinking is that maybe he can just hack together some Python
# code to "simplify" all of his homework.  Of course, this ignores the
# fact that introducing a computer program probably turns one problem
# into two worse problems.
#
# In any case, one problem concerns the representation of alegbraic
# expressions which contain a mix of operators, variables, and
# numbers.  For example: `3*x + y - 5`
#
# To do this, he has decided to use integers, strings, and tuples.
# Here are some examples of how things get written:
#
#   2            ->  2
#   x            ->  'x'
#   2 + 3        ->  (2, '+', 3)
#   2 + 3 + 4    ->  ((2, '+', 3), '+', 4)
#   2 * x        ->  (2, '*', 'x')
#   3 * x + y    ->  ((3, '*', 'x'), '+', 'y')
#   -x           ->  ('-', 'x')
#   x - y        ->  ('x', '-', 'y')
#
# Part of the motivation for writing equations in this form is that
# the goal is to manipulate the equation itself--leaving the operators
# and variable names "as is."  So, even though it looks a bit janky
# when written in Python, it's achieving that effect.
#
# An important facet of this representation concerns nesting.  For
# complicated expressions, parts get nested into a tree-like
# structure.  For example, the `3 * x + y` expression above shows
# this.  Also, it's important to note that the operators like `+` and
# `*` only take two arguments.  So, to represent `2 + 3 + 4`, you have
# to break it into two `+` operations as shown above.

# -----------------------------------------------------------------------------
# Part 1 - The Formatter
#
# Your first task.  Write a `format_expr()` function that takes the
# above tuple representation and turns it into a string that would be
# valid code if you pasted it in a Python program.  For example:
#
#   e = ('2', '+', 'x')
#   format_expr(e)     -> "(2 + x)"
#
# Further tests can be found below.  Don't make this too complicated.
# Mainly we're getting rid of the tuples and strings to make things
# look "nice."

def format_expr(e) -> str:
    if isinstance(e, int):
        return str(e)
    elif isinstance(e, str):
        return e
    if e[0] == '-': # Need to bind the minus sign onto the first term without space
        first_term_str = "-" + format_expr(e[1])
        if len(e) > 2:
            return format_expr(tuple([first_term_str] + [_ for _ in e[2:]]))
        return first_term_str
    e_str = "("
    i = 0
    while i < len(e):
        e_str += format_expr(e[i]) + " "
        i += 1
    e_str = e_str[:-1] + ")"
    return e_str

def format_expr_nobrackets(e) -> str:
    if isinstance(e, int):
        return str(e)
    elif isinstance(e, str):
        return e
    if e[0] == '-': # Need to bind the minus sign onto the first term without space
        first_term_str = "-" + format_expr(e[1])
        if len(e) > 2:
            return format_expr(tuple([first_term_str] + [_ for _ in e[2:]]))
        return first_term_str
    assert len(e) == 3
    combiner_ops = ['*', '/']
    if e[1] in combiner_ops:
        return " ".join([format_expr(e[0]), e[1], format_expr(e[2])])
    e_str = "("
    i = 0
    while i < len(e):
        e_str += format_expr(e[i]) + " "
        i += 1
    e_str = e_str[:-1] + ")"
    return e_str

def test_format():
    assert format_expr(2) == '2'
    assert format_expr('x') == 'x'
    assert format_expr((2, '+', 3)) == '(2 + 3)'
    assert format_expr(('x', '*', 'y')) == '(x * y)'
    assert format_expr(((3, '*', 'x'), '+', 'y')) == '((3 * x) + y)'
    assert format_expr((3, '-', 'x')) == '(3 - x)'
    assert format_expr(('-', ('x', '+', 'y'))) == '-(x + y)'
    assert format_expr((('-', ('x', '+', 'y')), '*', '1')) == '(-(x + y) * 1)'
    
def test_bracket_removal_format():
    print(format_expr_nobrackets((2, '+', (3, '*', 'x'))))
    assert format_expr_nobrackets(((2, '+', 3), '*', 'x')) == '(2 + 3) * x'
    assert format_expr_nobrackets((2, '+', (3, '*', 'x'))) == '2 + 3 * x'

# Uncomment
#test_format()
#test_bracket_removal_format() TODO: Finish this. Should we instead add the brackets lazily?
# Bonus:  Can you modify your formatter to remove unnecessary
# parentheses?   Note: This is fraught with a certain peril
# as illustrated by this example:
#
#    (2, '+', (3, '*', 'x'))   -> 2 + 3 * x
#    ((2, '+', 3), '*', 'x')   -> (2 + 3) * x
#
# Sometimes the parentheses are needed to express the proper
# order of evaluation.

# -----------------------------------------------------------------------------
# Part 2 - Constant Evaluation
#
# In algebra, it's common to "simplify" your work.  One simplication
# concerns constant values.  For example, suppose you had this equation:
#
#     x * (4 + 5)
#
# Instead of that, you'd probably just write:
#
#    x * 9
#
# Doing this doesn't change the meaning of the expression in any way.
# It just reduces the complexity of what's written.
#
# Your task.  Write a function `simplify_constants()` that takes an
# expression and evaluates all of the operations involving numeric
# constants.  There still may be variables which need to be left alone
# and that's fine.  A critical feature is that the mathematical
# meaning of the expression can't change.
#
# Tests follow below

def simplify_constants(e):
    if isinstance(e, int) or isinstance(e, str):
        return e
    if e[0] == '-':
        term = simplify_constants(e[1])
        if isinstance(term, int):
            return -term
        return ('-', term)
    assert(len(e) == 3)
    first_term = simplify_constants(e[0])
    second_term = simplify_constants(e[2])
    if isinstance(first_term, int) and isinstance(second_term, int):
        op = e[1]
        if op == '*':
            return first_term * second_term
        elif op == '+':
            return first_term + second_term
        elif op == '-':
            return first_term - second_term
        else:
            print("Unknown operator")
    return (first_term, e[1], second_term)

def test_simplify_constants():
    assert simplify_constants(2) == 2
    assert simplify_constants('x') == 'x'
    assert simplify_constants((2, '+', 3)) == 5
    assert simplify_constants((2, '+', 'x')) == (2, '+', 'x')
    assert simplify_constants(((3, '*', 4), '+', 'x')) == (12, '+', 'x')
    assert simplify_constants(('-', 3)) == -3
    assert simplify_constants(('-', ('-', 3))) == 3
    assert simplify_constants(((2, '+', 3), '*', (4, '+', 5))) == 45

# Uncomment
test_simplify_constants()

# Bonus: There are some simplifications that are algebraically legal,
# but may be rather difficult to recognize because of the way we've
# structured things.   Only work on this if you have time.
def test_bonus_simplify_constants():
    assert simplify_constants((('x', '+', 2), '+', 3)) == ('x', '+', 5)
    assert simplify_constants((('x', '+', 2), '-', 3)) == ('x', '-', 1)
    assert simplify_constants((('x', '+', 2), '*', 3)) == (('x', '+', 2), '*', 3)
#test_bonus_simplify_constants()
# -----------------------------------------------------------------------------
# Part 3 - Identities
#
# There are certain algebraic "identities" that are always true regardless
# of the expression `e` involved.  Here are some:
#
#      e + 0         -> e
#      0 + e         -> e
#      e * 0         -> 0
#      0 * e         -> 0
#      e * 1         -> e
#      1 * e         -> e
#      e - e         -> 0
#      --e           -> e
#
# Your task.  Write a function that looks for these identities and
# rewrites the expression in a more simple form. Note: These could be
# deeply buried inside so you've got to go searching for them.
#

def simplify_identities(e):
    if isinstance(e, int) or isinstance(e, str):
        return e
    if e[0] == '-':
        if not (isinstance(e, int) or isinstance(e, str)):
            if e[1][0] == '-':
                return simplify_identities(e[1][1])
            return ('-', simplify_identities(e[1]))
    assert(len(e) == 3)
    op = e[1]
    first = simplify_identities(e[0])
    second = simplify_identities(e[2])
    if op == '*':
        if first == 0:
            return 0
        elif second == 0:
            return 0
        elif first == 1:
            return simplify_identities(second)
        elif second == 1:
            return simplify_identities(first)
    if op == '+':
        if first == 0:
            return simplify_identities(second)
        elif second == 0:
            return simplify_identities(first)
    if op == '-':
        if first == second:
            return 0
    return (first, op, second)

def test_simplify_identities():
    assert simplify_identities(((2, '+', 'x'), '+', 0)) == (2, '+', 'x')
    assert simplify_identities((2, '+', (0, '+', 'x'))) == (2, '+', 'x')
    assert simplify_identities(((2, '+', 'x'), '*', 0)) == 0
    assert simplify_identities((2, '+', (0, '*', 'x'))) == 2
    assert simplify_identities(((2, '+', 'x'), '*', 1)) == (2, '+', 'x')
    assert simplify_identities((2, '+', (1, '*', 'x'))) == (2, '+', 'x')
    assert simplify_identities((2, '+', ('x', '-', 'x'))) == 2
    assert simplify_identities(('-', ('-', (2, '+', 'x')))) == (2, '+', 'x')

# Uncomment
test_simplify_identities()

# -----------------------------------------------------------------------------
# Part 4 - Combination
#
# In the previous two parts, you wrote two functions; one to simplify
# constants and one to simplify algebraic identifies.  How do you
# combine them together?  Is there a certain order in which the
# operations are supposed to be applied?  Do you have to simplify
# things more than once?
#
# In this part, you should write a top-level `simplify()` function
# that uses the other two functions to simplify equations.

# 

def simplify(e):
    next = simplify_constants(simplify_identities(e))
    while next != e:
        e = next
        next = simplify_constants(simplify_identities(e))
    return e

def test_simplify():
    assert simplify(('x', '+', ((-3, '+', 2), '+', 1))) == 'x'
    assert simplify((2, '+', (0, '*', 'x'))) == 2

# Uncomment
test_simplify()

# -----------------------------------------------------------------------------
# Big Picture
#
# A compiler translates programs in one language to another language.  Most
# programmers tend to think about something low-level like translation
# from C to machine code.   However, it can also work at a higher level
# like translating Typescript to Javascript.
#
# There are a few critical parts to this translation process.
#
# 1. Programs have to be represented as data structures that can be
#    manipulated.  In this warmup, tuples were used to do that.
#    That's not the only approach.
#
# 2. Programs are often rewritten into other programs.  The various
#    simplification steps are an example of this.  Actually, some
#    of the simplifications we performed could be considered
#    program optimizations instead.
#
# 3. A compiler is not allowed to change the meaning of the program.
#    That is, you can do whatever you want to the program, but it
#    has to produce the same outcome.  If you think back to your
#    algebra class, there are all sorts of "tricks" one can apply,
#    but you're not allowed to alter the meaning of an equation.
#    It's the same idea.
#
# In the compilers course, we'll build upon all of these ideas.
# There will be much more structure and different kinds of
# programming challenges, but the overall mental model is
# "program translation."

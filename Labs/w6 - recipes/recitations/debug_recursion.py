import builtins
from functools import wraps
import sys


def show_recursive_structure(f):
    """
    Show call entry/exits on stderr.

    Wrapper to instrument a function to show the call entry and exit
    from that function. Can customize view with instrument flags.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):

        def indent():
            return "   " * wrapper._depth

        def myprint(*args, **kwargs):
            builtins.print(indent(), end="")
            return builtins.print(*args, **kwargs)

        if show_recursive_structure.INDENT_PRINTS:
            f.__globals__["print"] = myprint

        # How to display the arguments in the function call?
        # 1) Build a string with the args.
        arg_str = ", ".join(str(a) for a in args)

        # 2) Possibly trim the args in the argument string.
        if (
            show_recursive_structure.TRIM_ARGS is not None
            and len(arg_str) > show_recursive_structure.TRIM_ARGS
        ):
            arg_str = arg_str[: show_recursive_structure.TRIM_ARGS] + " ..."

        # Print information on the current function call (including args).
        if show_recursive_structure.SHOW_CALL:
            sys.stderr.write(indent())
            sys.stderr.write(f"call to {f.__name__}: {arg_str}\n")

        wrapper._count += 1
        wrapper._depth += 1
        wrapper._max_depth = max(wrapper._depth, wrapper._max_depth)

        # Call the wrapped function.
        result = f(*args, **kwargs)

        wrapper._depth -= 1

        # The next lines create a string representing the output of the function call, and then
        # print that string.
        res_str = str(result)

        # Possibly trim the result string.
        if (
            show_recursive_structure.TRIM_RET is not None
            and len(res_str) > show_recursive_structure.TRIM_RET
        ):
            res_str = res_str[: show_recursive_structure.TRIM_RET] + " ..."

        # Print out the result string with indentation.
        if show_recursive_structure.SHOW_RET:
            sys.stderr.write(indent())
            sys.stderr.write(f"return from {f.__name__}: {res_str}\n")

        return result

    wrapper._count = 0
    wrapper._depth = 0
    wrapper._max_depth = 0
    return wrapper


# all prints from instrumented function are indented to recursive level
show_recursive_structure.INDENT_PRINTS = True
show_recursive_structure.SHOW_CALL = True
show_recursive_structure.SHOW_RET = True
show_recursive_structure.TRIM_ARGS = 55  # None if no trimming
show_recursive_structure.TRIM_RET = 60  # None if no trimming

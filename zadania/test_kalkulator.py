# import kalkulator

# kalkulator.add


from kalkulator import add, sub, mul, div

assert add(1, 2) == 3
assert add(1, 2, 3) == 6
assert sub(1, 2) == -1
assert mul(2, 2) == 4
assert mul(-2, 2) == -4
assert mul(-2, -3) == 6
assert mul(-2, -3, -2) == -12

assert div(1, 2) == 0.5
assert div(10, 0) == None

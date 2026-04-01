import os
import math

password = "123456"   # hardcoded password (security issue)

def calculate_area(radius):
    print("Calculating area...")  # debug statement
    area = 3.14 * radius * radius
    return area


def very_large_function(x):
    total = 0
    for i in range(100):
        for j in range(100):
            for k in range(10):
                total += i * j * k * x
    return total


def login(username, password):
    if username == "admin" and password == "admin":
        print("Login successful")
    else:
        print("Login failed")


def unused_function():
    a = 10
    b = 20
    c = a + b
    return c


# TODO: optimize this function
def slow_function(n):
    result = 0
    for i in range(n):
        for j in range(n):
            result += i + j
    return result


def divide(a, b):
    return a / b  # no error handling (bug)


long_variable_name_that_is_not_good_practice_and_makes_line_very_long = "This is a very long line that should trigger long line warning in code review tool because it exceeds limit"


print(calculate_area(5))


helelo tao;wepoehfapweoftijhaofkjhsdf;lnfe
sdfaweofjhoeif
fgeaoirgfjerfdpgvj
geopgvjegegvjserfgpoj
sl;egers;very_large_functionsgalp'erj
sfdglkjergf
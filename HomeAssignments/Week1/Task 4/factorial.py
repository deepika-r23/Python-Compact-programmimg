#method using for loop
factorialnumber = int(input("Enter a number: "))
factorialvalue = 1

for i in range(1,factorialnumber+1):
    factorialvalue = factorialvalue * i

print("The Factorial value using for loop is ",factorialvalue)

#method using math library
from math import factorial

factorial(5)
print("The Factorial of 5 using math library is ", factorial(5))


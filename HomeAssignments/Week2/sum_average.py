s1 = "Python123abc45"

digits = [int(char) for char in s1 if char.isdigit()]

if digits:
    total = sum(digits)
    average = total / len(digits)

    print("Sum:", total)
    print("Average:", average)
else:
    print("No digits found in the string.")
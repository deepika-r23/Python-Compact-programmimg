strings = [
    "Python is easy",
    "I am learning programming",
    "Hello world"
]

list_of_lists = list(map(str.split, strings))

print(list_of_lists)
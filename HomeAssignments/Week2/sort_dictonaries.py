cars = [
    {'make': ' Google ', 'model': 216, 'color': 'Black'},
    {'make': 'Mi Max', 'model': '2', 'color': 'Gold'},
    {'make': 'Samsung', 'model': 7, 'color': 'Blue'}
]

sorted_cars = sorted(
    cars,
    key=lambda car: int(car['model']),
    reverse=True
)

print(sorted_cars)
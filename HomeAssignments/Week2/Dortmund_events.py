events = {
    "KUULlus – Tierisch cool!": {
        "date": "2026-09-19",
        "time": "16:00-23:00",
        "location": "Naturmuseum Dortmund"
    },
    "Unter der Lupe": {
        "date": "2026-09-19",
        "time": "16:00-21:00",
        "location": "Naturmuseum Dortmund"
    },
    "Connected – Digitale Kultur im Ruhrgebiet": {
        "date": "2026-09-19",
        "time": "18:00-23:00",
        "location": "Phoenix des Lumières"
    },
    "Erkennt ihr euer Dortmunder?": {
        "date": "2026-09-19",
        "time": "21:15-22:00",
        "location": "Brauerei-Museum Dortmund"
    },
    "Nachts im Museum": {
        "date": "2026-09-19",
        "time": "23:30-00:45 (next day)",
        "location": "Naturmuseum Dortmund"
    },
    "Die DEW21 Museumsnacht tanzt": {
        "date": "2026-09-19",
        "time": "23:00-03:00 (next day)",
        "location": "domicil Dortmund"
    }
}

target_date = "2026-09-19"

print("Events during Dortmund Museumsnacht:")
for name, details in events.items():
    if details["date"] == target_date:
        print(
            name,
            "-",
            details["time"],
            "-",
            details["location"]
        )
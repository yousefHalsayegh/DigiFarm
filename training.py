
nature = {"Virus": 0, "Data":3, "Vaccine":0}

n = max(nature, key=nature.get)

print(n)
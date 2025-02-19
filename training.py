
import json

with open('Systems/starting_eggs.json', 'r') as file:
    eggs = json.load(file)

    print(list(eggs[0].keys()))
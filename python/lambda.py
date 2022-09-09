people = [
	{'name':'Harry', 'house':'Gryffindor'},
	{'name':'Cho', 'house':'Ravenclaw'},
	{'name':'Draco', 'house':'Slytherin'},
]

def helpSort(obj):
	return obj['house']

people.sort(key=lambda person: person['name'])
# people.sort(key=helpSort)


print(people)

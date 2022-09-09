number = int(input('Number: '))

isPositive = number > 0
isNegative = number < 0

if isPositive:
	print('number is positive')
elif isNegative:
	print('number is negative')
else:
	print('number is zero')

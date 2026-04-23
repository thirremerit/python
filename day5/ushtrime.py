numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

even_numbers = []

for n in numbers:
    if n % 2 == 0:
        even_numbers.append(n + 2)

print(even_numbers)
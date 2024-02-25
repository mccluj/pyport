import timeit

# Using list comprehension
lc_time = timeit.timeit('[i**2 for i in range(1000)]', number=10000)

# Using explicit loop
loop_time = timeit.timeit('''
result = []
for i in range(1000):
    result.append(i**2)
''', number=10000)

print(f"List comprehension time: {lc_time}")
print(f"Explicit loop time: {loop_time}")

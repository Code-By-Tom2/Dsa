# Number of rows
rows = 5

for i in range(1, rows + 1):
    pattern = []
    for j in range(i):
        # Alternating 1 and 0 based on the sum of row and column index
        pattern.append(str((i + j) % 2))
    print(" ".join(pattern))

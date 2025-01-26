# Number of rows
rows = 5

# Start from 1
current = 1

for i in range(1, rows + 1):
    # Generate numbers for each row
    row = []
    for j in range(i):
        row.append(str(current))
        current += 1
    # Print the row
    print(" ".join(row))

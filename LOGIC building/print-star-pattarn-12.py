# Number of rows
rows = 4

for i in range(1, rows + 1):
    # Generate the left side of the pattern
    left = ''.join(str(j) for j in range(1, i + 1))
    # Generate the right side of the pattern
    right = ''.join(str(j) for j in range(i, 0, -1))
    # Calculate spaces in the middle
    spaces = ' ' * (2 * (rows - i))
    # Combine left, spaces, and right to form the row
    print(left + spaces + right)

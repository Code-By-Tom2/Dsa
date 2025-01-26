# Number of rows
rows = 5

# Generate the top half of the pattern
for i in range(rows):
    # Left side stars
    left = '*' * (rows - i)
    # Right side stars
    right = '*' * (rows - i)
    # Spaces in between
    spaces = ' ' * (2 * i)
    # Print the row
    print(left + spaces + right)

# Generate the bottom half of the pattern
for i in range(rows - 2, -1, -1):
    # Left side stars
    left = '*' * (rows - i)
    # Right side stars
    right = '*' * (rows - i)
    # Spaces in between
    spaces = ' ' * (2 * i)
    # Print the row
    print(left + spaces + right)

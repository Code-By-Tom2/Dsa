rows = 4

for i in range(1, rows + 1):
    # Generate the first half of the pattern (increasing characters)
    left = [chr(65 + j) for j in range(i)]
    # Generate the second half of the pattern (decreasing characters)
    right = left[:-1][::-1]
    # Combine both halves
    row = left + right
    # Print the row with appropriate spaces for alignment
    print(" " * (rows - i) + "".join(row))

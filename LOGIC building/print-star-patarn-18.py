# Number of rows
rows = 5

for i in range(rows):
    # Generate the letters in reverse order starting from E
    row = [chr(69 - i + j) for j in range(i + 1)]  # 69 is the ASCII value of 'E'
    # Print the row
    print(" ".join(row))


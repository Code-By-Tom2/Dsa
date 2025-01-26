# Number of rows
rows = 5

for i in range(rows, 0, -1):
    # Generate characters for each row
    row = [chr(65 + j) for j in range(i)]  # 65 is the ASCII value of 'A'
    # Print the row
    print("".join(row))

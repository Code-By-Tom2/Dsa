# Number of rows
rows = 5

for i in range(rows):
    # Generate the character and repeat it i+1 times
    row = chr(65 + i) * (i + 1)  # 65 is the ASCII value of 'A'
    # Print the row
    print(row)

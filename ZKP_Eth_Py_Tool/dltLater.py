# Open the file for reading
with open('lol.txt', 'r') as file:
    # Read the contents of the file into a string
    file_contents = file.read()

print(file_contents)
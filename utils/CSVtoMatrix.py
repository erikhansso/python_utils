import numpy as np

# This script transforms csv-files into a 2D-matrix
# of rows x columns, which is lines x columns in the csv file..
# This is not the best way, it's just for illustration.

# Create an empty list to hold the matrix
X = []

input_filepath = "inputfilepathhere"

for line in open(input_filepath):

    # For each line in the file, split on the commas
    row = line.split(',')

    # Remove any line break characters
    # need not be done since we are casting to float,
    # but good to know. Although this doesn't work as is,
    # need to change it a bit and not just lift it out of print statement

    # print([s.replace('\n', '') for s in row])
    #
    # print(row)

    # This yields strings, so we want to cast them into floats
    # Note that the map function returns a map, so we need to pass it
    # to the list()-function.
    sample = list(map(float, row))

    # Append to our list
    X.append(sample)


# Convert the list into an numpy array
X = np.array(X)

print(X)

# Check the shape
print(X.shape)



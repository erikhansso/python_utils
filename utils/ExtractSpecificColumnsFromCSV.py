import pyexcel as pe

file_name = "filenamehere"
sheet = pe.get_sheet(file_name=file_name)
# the column indices to keep
sheet.column.select([3, 4, 5, 6])
output_filename = "outputfilenamhere"
sheet.save_as(output_filename)

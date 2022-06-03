import re

fileName = "..." # full path to a file

with open(fileName, "r", encoding="utf8") as f1:
	data = f1.read()

	# insert any regular expression replaces
	data = re.sub(",", "\t", data) # this line replaces commas with tabs


	with open(fileName + "_updated.csv", "w", encoding="utf8") as f9:
		f9.write(data)
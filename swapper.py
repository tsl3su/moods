
def remove_left(outfile):

	with open(outfile, 'r+') as f:

		num = 0
		csv = []
		while True:
			data = f.readline()
			if (num >= 1 and num <= 8):
				csv.append(data)
			num += 1
			if data == '':
				break
	
		f.seek(0)
		for row in csv:
			f.write(row)
		f.truncate()



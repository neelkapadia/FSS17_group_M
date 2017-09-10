from multiprocessing import Queue


def process_header(line,header):
	try:
		comment_loc = line.index("#")   #detect the comments
	except:
		comment_loc = len(line)
	line = line[0:comment_loc]			#eliminate the comments
	for x in line.split(','):			#split using delimiter
		x = x.strip()					#remove whitespaces
		if x!= "":
			header.append(x)

def process_data_and_enqueue(line,table,j,i):
	try:
		comment_loc = line.index("#")   #detect the comments
	except:
		comment_loc = len(line)
	line = line[0:comment_loc]			#eliminate the comments
	for x in line.split(','):			#split using delimiter
		x = x.strip()					#remove whitespaces
		if x!= "":
			table[i].append(x)
			j=j+1
			if j%column_numbers == 0:
				i=i+1


q = []
input = open("input.csv","r")
line = input.readline()
header = []
process_header(line,header)
table=[]
table.append(header)


column_numbers=len(header)

#print(header)

line = input.readline()
j=0
i=0
while line:
	process_data_and_enqueue(line,table,j,i)
	line = input.readline()

minitable=[]
t=[]
i=0
for element in table[0]:
	minitable.append(element)
	i=i+1
	if i%column_numbers == 0:
		t.append(minitable)
		minitable=[]



for row in t:
	print(row)

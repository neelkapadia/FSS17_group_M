from multiprocessing import Queue
import sys


def process_header(line,header,list):
	try:
		comment_loc = line.index("#")   #detect the comments
	except:
		comment_loc = len(line)
	line = line[0:comment_loc]			#eliminate the comments
	for x in line.split(','):			#split using delimiter
		x = x.strip()					#remove whitespaces
		if x!= "":
			y=x[:1]
			header.append(x)
			if ord(y)<65:
				list.append(1)
			else:
				list.append(0)


def process_data_and_enqueue(line,table,j,i,list):
	try:
		comment_loc = line.index("#")   #detect the comments
	except:
		comment_loc = len(line)
	try:
		line = line[0:comment_loc]			#eliminate the comments
		for x in line.split(','):			#split using delimiter
			x = x.strip()					#remove whitespaces
			if x!= "":
				if list[j]==1:
					y=float(x)
				else:
					y=x
				table[i].append(y)
				j=j+1
				if j%column_numbers == 0:
					i=i+1
	except:
		print("Bad Line :"+str(line))

q = []
input = open(sys.argv[1], 'rb')
line = input.readline()
header = []
list=[]
process_header(line,header,list)
table=[]
table.append(header)


column_numbers=len(header)

#print(header)

line = input.readline()
j=0
i=0
while line:
	process_data_and_enqueue(line,table,j,i,list)
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

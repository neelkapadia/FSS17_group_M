from multiprocessing import Queue
import math


class Table:
    name=""
    headers=[]
    rows=[]
    rowCount=0
    def __init__(self,name):
        self.name=name

    def get_column_type(self,columnNumber):
        return self.headers[columnNumber].isNum

    def get_column_ignore(self,columnNumber):
        return self.headers[columnNumber].ignore

    def add_rows(self,input):
        for line in input:
            row=Row(self.rowCount)
            row.break_line_into_cells(line,self)
            self.rows.append(row)
            self.rowCount=self.rowCount+1


    def normalize(self):
        for row in self.rows:
            for cell in row.cells:
                if self.headers[cell.columnNumber].isNum==1 and self.headers[cell.columnNumber].ignore==False :
                    cell.value=(float)(int(cell.value)-self.headers[cell.columnNumber].minValue)/(float)(self.headers[cell.columnNumber].maxValue-self.headers[cell.columnNumber].minValue)

    def update_headers(self):
        for row in self.rows[0]:
            for cell in cells:
                print(cell.value)
        for header in self.headers:
            #header.print_header_data()
            if header.ignore==False:
                for row in self.rows:
                    if header.isNum==1:
                        #print("M " + str(row.cells[header.columnNumber].value))
                        if header.minValue>row.cells[header.columnNumber].value:
                            header.minValue=row.cells[header.columnNumber].value
                        #print("X " + str(header.maxValue) + "   " + str(row.cells[header.columnNumber].value))
                        if header.maxValue<row.cells[header.columnNumber].value:
                            header.maxValue=row.cells[header.columnNumber].value
                        header.sum = header.sum + row.cells[header.columnNumber].value
                        header.totalElements=header.totalElements+1
                    '''else:
                        count=header.frequency.get(row.cells[header.columnNumber].value,0)
                        count=count+1
                        header.frequency[row.cells[header.columnNumber].value]=count
                        header.totalElements = header.totalElements + 1'''



    def calculate_entropy(self):
        for row in self.rows:
            for cell in row.cells:
                print(cell.value)
        for header in self.headers:
            sum=0
            if header.isNum ==0 and header.ignore==False:
                for key in header.frequency.keys():
                    #print(key +" "+ str(header.frequency.get(key,0)))
                    p=header.frequency[key]/header.totalElements
                    sum=sum-(p*math.log(p,2))
                header.entropy=sum
                #print(str(header.columnNumber) +"  "+ str(header.entropy))



class Header:
    columnName=""
    columnNumber=0
    ignore=False
    isNum=0
    weight=0
    minValue=10000
    maxValue=-10000
    goal=0
    sum=0
    totalElements=0
    frequency={}

    def print_header_data(self):
        print(str(self.columnNumber)+" "+str(self.columnName)+" "+str(self.minValue)+" "+str(self.maxValue)+" "+str(self.totalElements))

    def __init__(self,ignore,isNum,weight,minValue,maxValue,goal):
        self.ignore=ignore
        self.isNum=isNum
        self.weight=weight
        self.minValue=minValue
        self.maxValue=maxValue
        self.goal=goal

class Row:
    cells=[]
    rowNumber=0
    def __init__(self,rowNumber):
        self.rowNumber=rowNumber


    def break_line_into_cells(self,line,table):
        i=0
        for x in line:  # split using delimiter
            x = x.strip()  # remove whitespaces
            if x != "" and table.get_column_ignore!=True :
                cell=Cell(i,self.rowNumber)
                if table.get_column_type(i) == 1:
                    cell.value=int(x)
                else:
                    cell.value = x
                self.cells.append(cell)
            i=i+1


class Cell:
    columnNumber=0
    rowNumber=0
    def __init__(self,columnNumber,rowNumber):
        self.columnNumber=columnNumber
        self.rowNumber=rowNumber


def create_table(name):
    table = Table(name)
    return table

def add_headers(table,line):
    def questionMark():
        header = Header(True, 1, 1, 10000, -10000, 0)
        return header

    def dollar():
        header=Header(False,1,1,10000, -10000,0)
        return header

    def lesser():
        header = Header(False, 1, -1, 10000, -10000, 1)
        return header

    def greater():
        header = Header(False, 1, 1, 10000, -10000, 1)
        return header

    def exclamation():
        header = Header(False,0, 1, 10000, -10000, 0)
        return header

    def default():
        header = Header(False, 0, 1,10000, -10000, 0)
        return header

    # map the inputs to the function blocks
    options = {"$": dollar,
               "?": questionMark,
               "<": lesser,
               ">": greater,
               "!": exclamation,
               "default":default,
               }

    headers=[]
    i=0
    for x in line:  # split using delimiter
        x = x.strip()  # remove whitespaces
        if x != "":
            firstElement=x[:1]
            if ord(firstElement)<65:
                header=options[firstElement]()
                header.columnName=x[1:]
                header.columnNumber=i
                table.headers.append(header)
                i = i + 1
            else:
                header=options["default"]()
                header.columnName=x
                header.columnNumber = i
                table.headers.append(header)
                i = i + 1
    return table



def get_clean_data():
    def process_header(line, header):
        try:
            comment_loc = line.index("#")  # detect the comments
        except:
            comment_loc = len(line)
        line = line[0:comment_loc]  # eliminate the comments
        for x in line.split(','):  # split using delimiter
            x = x.strip()  # remove whitespaces
            if x != "":
                header.append(x)

    def process_data_and_enqueue(line, table, j, i):
        try:
            comment_loc = line.index("#")  # detect the comments
        except:
            comment_loc = len(line)
        line = line[0:comment_loc]  # eliminate the comments
        for x in line.split(','):  # split using delimiter
            x = x.strip()  # remove whitespaces
            if x != "":
                table[i].append(x)
                j = j + 1
                if j % column_numbers == 0:
                    i = i + 1

    q = []
    input = open("input.csv", "r")
    line = input.readline()
    header = []
    process_header(line, header)
    table = []
    table.append(header)

    column_numbers = len(header)

    # print(header)

    line = input.readline()
    j = 0
    i = 0
    while line:
        process_data_and_enqueue(line, table, j, i)
        line = input.readline()

    minitable = []
    t = []
    i = 0
    for element in table[0]:
        minitable.append(element)
        i = i + 1
        if i % column_numbers == 0:
            t.append(minitable)
            minitable = []
    return t


if __name__=='__main__':
    inputTable = get_clean_data()
    table = create_table('DataTable')

    table = add_headers(table, inputTable[0])
    table.add_rows(inputTable[1:])
    #table.normalize()
    table.update_headers()


    #table.calculate_entropy()




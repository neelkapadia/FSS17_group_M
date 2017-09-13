from multiprocessing import Queue
import math
import sys


class Table:
    name=""
    headers=[]
    rows=[]
    goals=[]
    list=[]
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
            try:
                _cells=row.break_line_into_cells(line,self)
                row.cells = _cells
                self.rows.append(row)
                self.rowCount = self.rowCount + 1
            except:
                count=0



    def normalize(self):
        for row in self.rows:
            for cell in row.cells:
                if self.headers[cell.columnNumber].isNum==1 and self.headers[cell.columnNumber].ignore==False :
                    cell.value=(float)(int(cell.value)-self.headers[cell.columnNumber].minValue)/(float)(self.headers[cell.columnNumber].maxValue-self.headers[cell.columnNumber].minValue)

    def update_headers(self):
        for header in self.headers:
            _frequency = {}
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
                    else:

                        count=_frequency.get(row.cells[header.columnNumber].value,0)
                        count=count+1
                        _frequency[row.cells[header.columnNumber].value]=count
                        header.totalElements = header.totalElements + 1
                        header.frequency=_frequency



    def calculate_entropy(self):
        for header in self.headers:
            sum=0.0
            if header.isNum ==0 and header.ignore==False:
                for key in header.frequency.keys():
                    p=(float(header.frequency[key])/float(header.totalElements))
                    sum=sum-(p * (math.log(p,2)))
                header.diversity=sum
                #print("Div: " + str(header.diversity))
            elif header.isNum ==1 and header.ignore==False:
                for row in self.rows:
                    x = row.cells[header.columnNumber].value
                    sum = sum + (x-(float(header.sum)/float(header.totalElements)))**2
                header.diversity=(sum/float(header.totalElements))**(0.5)
                #print("Div: "+str(header.diversity))

    def calculate_domination(self,rowNumber1,rowNumber2):
        row1=self.rows[rowNumber1]
        row2=self.rows[rowNumber2]
        sum1=0.0
        sum2=0.0
        for i in self.goals:
            if self.headers[i].ignore == False and self.headers[i].isNum == 1:
                w = self.headers[i].weight
                x= row1.cells[i].value
                y= row2.cells[i].value
                n= len(self.goals)
                sum1 = sum1 -  ((2.718)**(w * (x - y) / n))
                sum2 = sum2 - ((2.718) ** (w * (y - x) / n))
        if sum1>sum2:
            self.list[rowNumber1].append(rowNumber2)
        else:
            self.list[rowNumber2].append(rowNumber1)

    def find_dominating_rows(self):
        for i in range(0,len(self.rows)):
            miniList=[]
            self.list.append(miniList)
        for i in range(0,len(self.rows)):
            for j in range(i+1,len(self.rows)):
                self.calculate_domination(i,j)

    def print_top5_dominating_row(self):
        print("Top 5 dominating rows:")
        for j in range(0, 10):
            for i in range(0,len(self.list)):
                if len(self.list[i])==j:
                    sys.stdout.write(str(i)+" ")
                    for cell in self.rows[i].cells:
                        sys.stdout.write(str(cell.value) +" ")
            print("")

    def print_bottom5_dominating_row(self):
        print("Bottom 5 dominating rows:")
        n=len(self.list)
        for j in range(n-10, n):
            for i in range(0,len(self.list)):
                if len(self.list[i])==j:
                    sys.stdout.write(str(i)+" ")
                    for cell in self.rows[i].cells:
                        sys.stdout.write(str(cell.value) +" ")
            print("")


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
        _cells=[]
        i=0
        for x in line:  # split using delimiter
            x = x.strip()  # remove whitespaces
            if x != "" and table.get_column_ignore!=True :
                cell=Cell(i,self.rowNumber)
                if table.get_column_type(i) == 1:
                    cell.value=float(x)
                else:
                    cell.value = x
                _cells.append(cell)
            i=i+1
        return _cells

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
    def questionMark(i):
        header = Header(True, 1, 1, 10000, -10000, 0)
        return header

    def dollar(i):
        header=Header(False,1,1,10000, -10000,0)
        return header

    def lesser(i):
        header = Header(False, 1, -1, 10000, -10000, 1)
        table.goals.append(i)
        return header

    def greater(i):
        header = Header(False, 1, 1, 10000, -10000, 1)
        table.goals.append(i)
        return header

    def exclamation(i):
        header = Header(False,0, 1, 10000, -10000, 0)
        return header

    def default(i):
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
                header=options[firstElement](i)
                header.columnName=x[1:]
                header.columnNumber=i
                table.headers.append(header)
                i = i + 1
            else:
                header=options["default"](i)
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
    input = open(sys.argv[1], 'rb')
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
    table.update_headers()
    table.normalize()
    table.calculate_entropy()
    table.find_dominating_rows()
    table.print_top5_dominating_row()
    table.print_bottom5_dominating_row()




from multiprocessing import Queue


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

    def update_headers(self):
        for header in self.headers:
            if header.isNum==1 and header.ignore==False:
                for row in self.rows:
                    if header.minValue>row.cells[header.columnNumber].value:
                        header.minValue=row.cells[header.columnNumber].value
                    if header.maxValue<row.cells[header.columnNumber].value:
                        header.maxValue=row.cells[header.columnNumber].value
                    header.sum = header.sum + row.cells[header.columnNumber].value



class Header:
    columnName=""
    columnNumber=0
    ignore=False
    isNum=0
    weight=0
    minValue=0
    maxValue=0
    goal=0
    sum=0

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
                table.update_headers()
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
        header = Header(True, 1, 1, 0, 0, 0)
        return header

    def dollar():
        header=Header(False,1,1,0,0,0)
        return header

    def lesser():
        header = Header(False, 1, -1, 0, 0, 1)
        return header

    def greater():
        header = Header(False, 1, 1, 0, 0, 1)
        return header

    def exclamation():
        header = Header(False,0, 1, 0, 0, 0)
        return header

    def default():
        header = Header(False, 0, 1, 0, 0, 0)
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

    for header in table.headers:
        print(header.sum)


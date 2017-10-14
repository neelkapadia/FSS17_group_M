import sys

import operator
import math
from copy import deepcopy


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

    def print_top5_dominating_row(self,headerLine,outputFile):
        outputFile.write("Top 10 dominating rows:\n")
        for attribute in headerLine:
            outputFile.write(str(attribute) + "\t")
        outputFile.write("\n")
        for row in table.rows:
            for cell in row.cells:
                outputFile.write(str(cell.value) + "\t")

            outputFile.write("\n")
        outputFile.write("\n \n")

    def print_bottom5_dominating_row(self,inputTable,headerLine,outputFile):
        outputFile.write("Bottom 10 dominating rows:\n")
        for attribute in headerLine:
            outputFile.write(str(attribute) + "\t")
        outputFile.write("\n")
        n=len(self.list)
        for j in range(n-10, n):
            for i in range(0,len(self.list)):
                if len(self.list[i])==j:
                    #outputFile.write(str(i)+"\t")
                    for cell in inputTable[i]:
                        outputFile.write(str(cell) +"\t")
            outputFile.write("\n")


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
    try:
        input = open(sys.argv[1], 'rb')
    except:
        input = open("input.csv", 'rb')
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

def get_independent_variables(table):
    indepentdent=[]
    for i in range(0,len(table.headers)):
        if (i not in table.goals) and (not table.headers[i].ignore):
            indepentdent.append(i)
    return indepentdent

def sort_table(table, col):
    return sorted(table, key=operator.itemgetter(col))

def get_dummy_table(table):
    dummy=[]
    for row in table.rows:
        ro=[]
        for cell in row.cells:
            ro.append(cell.value)
        dummy.append(ro)

    return dummy

def get_bin_mean(table,ind):
    sum=0.0
    for row in table:
        sum = sum+ float(row[ind])
    mean= float(sum)/len(table)
    return mean

def get_bin_sd(table,ind):
    sum = 0.0
    for row in table:
        sum = sum + float(row[ind])
    mean = float(sum) / len(table)

    sum=0.0
    for row in table:
        sum = sum+ math.pow(float(row[ind])-mean,2)
    sd= float(sum)/len(table)
    sd= math.pow(sd,0.5)
    return sd

def normalize(_table,goals):
    table=  deepcopy(_table)
    for goal in goals:
        min=10000
        max=0
        for row in table:
            if row[goal]>max:
                max=row[goal]
            if row[goal]<min:
                min=row[goal]
        if max!=min:
            for row in table:
                row[goal]=((row[goal]-min)/(max-min))

    return table

def get_performance(_bin,outputFile,goals):
    bin=normalize(_bin,goals)
    sum=0
    for goal in goals:
        weight= table.headers[goal].weight
        for row in bin:
            sum=sum+(weight*row[goal])

    return sum

def split_by_goal(_index,_goalbins,_goals,_tree_height,outputFile,realgoals):
    goals=deepcopy(_goals)
    index=deepcopy(_index)
    goalbins=deepcopy(_goalbins)
    tree_height=_tree_height
    poppedIndex=goals.pop(_index)
    result=[]

    for _bin in goalbins[index]:
        if(get_bin_sd(_bin,poppedIndex)!=0):
            for i in range(1, tree_height):
                outputFile.write("|     ")
            outputFile.write(str(table.headers[poppedIndex].columnName) + "                               : n= "+ str(len(_bin)) +", mu =  "+ str(get_bin_mean(_bin,poppedIndex))+", sd = "+str(get_bin_sd(_bin,poppedIndex))+"\n")
            if len(_goals)>0:
                apply_supervised_discretization(_bin,goals,tree_height,outputFile,realgoals)
                result.append(get_performance(_bin,outputFile,realgoals))
                print(str(result[0]) + "   " + str(table.headers[poppedIndex].columnName) )
                #print("Bin:: "+ str(len(bin)))

    print(len(result))




def apply_supervised_discretization(table,goals,tree_height,outputFile,realgoals):

    doms=[]
    goalbins=[]
    dummy_table=deepcopy(table)
    for goal in goals:
        #print("For goal "+ str(goal))
        epsilon = 0
        sum=0.0
        for row in dummy_table:
            #print(row.cells[table.goals.index(goal)].value)
            sum = sum + float(row[goal])
        mean= sum/(len(dummy_table))
        variance=0.0
        for row in dummy_table:
            variance = variance + math.pow(float(row[goal])-mean,2)
        sd=math.pow(variance/len(dummy_table),0.5)
        epsilon=0.23*sd


        dummy_table=sort_table(dummy_table,goal)
        '''for row in dummy_table:
            print(str(row) + "  "+ str(dummy_table.index(row)))'''

        bins=[]
        binsLength=0
        for i in range(0,len(dummy_table)):
            if i==0:
                bins.append([])
                bins[binsLength].append(dummy_table[i])
            else:
                if (((float(dummy_table[i][goal])-float(dummy_table[i-1][goal])) > epsilon) and (len(bins[binsLength])>10)):
                    bins.append([])
                    binsLength=binsLength+1
                    bins[binsLength].append(dummy_table[i])
                else:
                    bins[binsLength].append(dummy_table[i])

        #print(" Goal : "+ str(table.headers[goal].columnName) +"  "+str(binsLength))
        #print(len(bins))
            #print(str(dummy_table[i][goal]) +" "+str(goal))
            #print(str(float(dummy_table[i][3])) +"   "+ str(float(dummy_table[i - 1][3]) )+ " "+ str(epsilon) + "   "+str(goal) )
        goalbins.append(bins)
        dom=0
        for bin in bins:
            sum=0
            for row in bin:
                sum= sum + float(row[goal])
            mean= sum/len(bin)
            var=0
            for row in bin:
                var= var + math.pow(float(row[goal])-mean,2)
            var= var/len(bin)
            sd=math.pow(var,0.5)

            dom = dom+ (sd*len(bin))
        dom=dom/len(dummy_table)
        doms.append(dom)

        #print(str(len(bins)) + " HA HA  " + str(goal))
    if len(doms)>0:
        split_by_goal(doms.index(max(doms)),goalbins,goals,tree_height+1,outputFile,realgoals)


if __name__=='__main__':
    outputFile = open('output.txt', 'w')
    inputTable = get_clean_data()
    table = create_table('DataTable')
    table = add_headers(table, inputTable[0])
    table.add_rows(inputTable[1:])
    table.update_headers()
    dummy_table = get_dummy_table(table)
    independent_variables=get_independent_variables(table)
    apply_supervised_discretization(dummy_table,independent_variables,0,outputFile,table.goals)



    outputFile.close()

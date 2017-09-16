import random
import decimal

def getList():
    op=[]
    for i in range(0,50):
        op.append(decimal.Decimal(random.randrange(1000000000000, 9000000000000))/10000000000000)
    return op

def createBins(dataList):
    n=len(dataList)
    binLength=



if __name__=='__main__':
    dataList=getList()
    dataList.sort()
    createBins(dataList)
    print(dataList)
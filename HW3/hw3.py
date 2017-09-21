import random
import decimal
import math

total_values=50

def getList():
    op=[]
    for i in range(0,total_values):
        op.append(float(decimal.Decimal(random.random())))

    return op

def getUnsupervisedBins(num_column):
    x_bin=[]
    bin_size=math.ceil(math.sqrt(total_values))+1
    bin_size_counter=0
    unsuper_dict={}
    dict_index=1
    num_column_index=0
    
    while (bin_size_counter<bin_size) and (num_column_index<len(num_column)):
        key="Label "+str(dict_index);
        x_bin.append(num_column[num_column_index])
        num_column_index=num_column_index+1
        bin_size_counter=bin_size_counter+1
        if (bin_size_counter==bin_size-1) or (num_column_index==len(num_column)):
            unsuper_dict[key] = x_bin
            x_bin=[]

            bin_size_counter=0
            dict_index=dict_index+1

    last_index=len(unsuper_dict)
    if(len(unsuper_dict["Label " +str(last_index)]) < bin_size):
        second_last_index = last_index-1
        unsuper_dict["Label "+str(second_last_index)] = unsuper_dict["Label "+str(second_last_index)] + unsuper_dict["Label "+str(last_index)]
        del unsuper_dict["Label "+str(last_index)]
        
    return unsuper_dict

def print_unsuper(unsuper_dict):
    k = sorted(unsuper_dict.keys())
    for i in k:
        high = unsuper_dict[i][len(unsuper_dict[i])-1]
        low = unsuper_dict[i][0]
        span = high - low
        n = len(unsuper_dict[i])
        print str(i) + "\tn = " + str(n) + "\tSpan = " + str(span) + "\tHigh = " + str(high) + "\tLow = " + str(low)

def unsupervised_discretization():
    num_column=[]
    unsuper_dict = {}
    num_column = getList()
    num_column.sort()
    unsuper_dict = getUnsupervisedBins(num_column)
    print("Unsupervised learner : ")
    print_unsuper(unsuper_dict)
    return num_column

def print_super(super_dict):
    print("")
    print("Supervised Learner:")
    count = 0
    k = sorted(super_dict.keys())
    for i in k:
        count = count + 1
        most = super_dict[i][len(super_dict[i])-1]
        n = len(super_dict[i])
        print "Label " + str(count) + "\tn = " + str(n) + "\tMost = " + str(most)

def supervised_discretization(data):
    super_dict = {}
    super_dict[0.2]= []
    super_dict[0.6]= []
    super_dict[0.9]= []
    super_dict[1]= []

    for i in range (0,len(data)):
        if data[i]<0.2:
            super_dict[0.2].append(data[i])
        elif data[i]<0.6:
            super_dict[0.6].append(data[i])
        elif data[i]<0.9:
            super_dict[0.9].append(data[i])
        else:
            super_dict[1].append(data[i])
    print_super(super_dict)


data = unsupervised_discretization()
supervised_discretization(data)

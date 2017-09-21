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
        key="Label"+str(dict_index);
        x_bin.append(num_column[num_column_index])
        num_column_index=num_column_index+1
        bin_size_counter=bin_size_counter+1
        if (bin_size_counter==bin_size-1) or (num_column_index==len(num_column)):
            unsuper_dict[key] = x_bin
            x_bin=[]

            bin_size_counter=0
            dict_index=dict_index+1

    last_index=len(unsuper_dict)
    if(len(unsuper_dict["Label"+str(last_index)]) < bin_size):        
        second_last_index = last_index-1
        unsuper_dict["Label"+str(second_last_index)] = unsuper_dict["Label"+str(second_last_index)] + unsuper_dict["Label"+str(last_index)]
        del unsuper_dict["Label"+str(last_index)]
        
    return unsuper_dict

num_column=[]
unsuper_dict = {}
num_column = getList()
num_column.sort()
unsuper_dict = getUnsupervisedBins(num_column)
print("Unsupervised learner : ")
for k, v in unsuper_dict.iteritems():
    print k, v

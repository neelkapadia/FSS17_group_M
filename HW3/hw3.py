import random
import decimal
import math

total_values=50

def getList():
    op=[]
    for i in range(0,total_values):
        op.append(decimal.Decimal(random.random()))

    for i in op:
        print(i)
    return op

def getUnsupervisedBins(num_column):
    x_bin=[]
    bin_size=math.sqrt(total_values)+1
    bin_size_counter=0
    unsuper_dict={}
    dict_index=1
    num_column_index=0
    
    while ((bin_size_counter/total_values)<=(bin_size)) and (num_column_index<len(num_column)):
        key="Label "+dict_index;
        xbin.append(num_column[num_column_index])
        num_column_index=num_column_index+1
        bin_size_counter=bin_size_counter+1
        if (bin_size_counter/total_values)==bin_size:
            unsuper_dict = {key:xbin}
            bin_size_counter=0
            dict_index=dict_index+1

    if(len(unsuper_dict.get("Label "+dict_index)) < bin_size):
        last_index=dict_index
        second_last_index = last_index-1
        unsuper_dict["Label "+last_index].append(unsuper_dict.get("Label "+second_last_index))
        del unsuper_dict["Label "+last_index]
        
    return unsuper_dict

num_column=[]
num_column = getList().sort()
unsuper_dict = getUnsupervisedBins(num_column)
for k, v in unsuper_dict.iteritems():
    print k, v

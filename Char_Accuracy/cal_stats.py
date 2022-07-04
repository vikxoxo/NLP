# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 23:23:28 2022

@author: Vikanksh

"""
# pip install pybind11
# pip install pybind11 fastwer
# pybind11, and fastwer are prerequisite dependencies

import argparse
 
parser = argparse.ArgumentParser(description="Calcute Stats based on GT, and Pred excel",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--gt", help="complete path to GT excel")
parser.add_argument("--pred", help="complete path to Pred excel")
parser.add_argument("--out", help="complete path to Output excel")
args = parser.parse_args()

config = vars(args)
print(config)

import fastwer
import pandas as pd

#taking args
arg1 = args.gt
arg2 = args.pred
arg3 = args.out

#reading excel
gt = pd.read_excel(arg1)
pred = pd.read_excel(arg2)


def cal_stat(gt, pred):
    #sort dataframe
    sorted_gt = gt.sort_values(by='Id')
    
    #sort dataframe
    sorted_pred = pred.sort_values(by='Id')
    
    ref = sorted_gt["GT"].values.tolist()  # GT are true reference values
    hypo = sorted_pred["PRED"].values.tolist()  #hypothesis is what we create ie predictions
    
    #based on given repo using following:
    
    # hypo = ['This is an example .', 'This is another example .']
    # ref = ['This is the example :)', 'That is the example .']
    
    # Corpus-Level WER
    # print(fastwer.score(hypo, ref))
    
    # Corpus-Level CER
    err = fastwer.score(hypo, ref, char_level=True)
    acc = 100-err
    
    #calc required stats
    line = len(gt)  #total lines in df
    lineGT = gt['GT'].count() #non-empty GT column rows
    char = sum(len(i) for i in ref) #total no of chars in GT
    
    # initialize list of lists
    data = [['Accuracy', acc], ['Total line GT Excel.', line], \
            ['Total non-empty line GT Col.', lineGT], ['Total charc GT Col.', char]]
    
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['Stat', 'Value'])
    
    #saving df at output loc excel
    df.to_excel(arg3)
    print("Output excel is saved")


cal_stat(gt, pred)

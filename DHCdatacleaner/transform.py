# -*- coding: utf-8 -*-

"""
Copyright (c) 2018 Eddie Yi Huang

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import print_function
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder
import argparse
from update_checker import update_check

# from ._version import __version__

update_checked = False

#灵活利用function,1对1生成衍生特征列
def function_derive(input_dataframe,sel_cols,new_cols,function,copy=False):
    '''
    Parameter
        -----
        :param input_dataframe: pd.Dataframe
        :param sel_col: should be a list
            input column name
        :param new_col: should be a list
            ouput column name
        :param function: sould be a function
            ex.def change(x):
                if x>20 and x<=30:
                    y=1
                elif x>30:
                    y=2
                else:
                    y=0
                return y
        :param append: bool
            if True append the derived col to the original dataset, default True
        :param copy: bool
            if True make a copy of the dataframe
    Return
    -----
        :input_dataframe:dataframe with new features
    '''
    if copy:
        input_dataframe=input_dataframe.copy()
    assert function.func_name
    assert type(input_dataframe)==pd.DataFrame
    assert type(sel_cols)==list and type(new_cols) ==list
    assert len(sel_cols)==len(new_cols)
    def derive(sel_col,new_col):
        input_dataframe[new_col]=map(function,input_dataframe[sel_col])
    map(derive,sel_cols,new_cols)
    return input_dataframe

#one-hot 变化：在离散变量中最常用的变化
def one_hot_derive(input_dataframe,sel_col,seperator=None,copy=False):
    '''
    One Hot transform for categorical col,only one col is supported.
    Parameters
        -----
        :param input_dataframe: pd.DataFrame
        :param sel_col: list,
            must be one col as this is one-hot transfer
        :param seperator: should be a string or None or whatever separates the features in the content of the data.
            The seperator Used in the values,
            ex.
            if you use',' as seperator,
         'A,B,C' will be detected as 3 values ['A','B','C']
        :param copy:bool
         whether copy the dataset or not
    Return
    -----
    :input_dataframe:dataframe with new features
    :vals:a list of values detected,names of the derived cols
    '''
    assert len(sel_col)==1
    if copy:
        input_dataframe=input_dataframe.copy()
    def to_list(x):
        #if x is a number convert it into a string.
        if type(x)==int or type(x)==float:
            x=str(x)
        try:
            l1=x.split(seperator)
            def f(x):return len(x)>0
            l2=list(filter(f,set(l1)))
            l2=list(set(l2))
            return l2
        except:
            return []
    ls=map(to_list,input_dataframe[sel_col[0]])
    ls=list(np.unique(ls))
    # print(ls)
    def add(x,y):
        return list(set(x+y))
    vals=reduce(add,ls)
    vals=list(set(vals))# get the compelte one-hot vals list.
    # print(vals)
    #then we create new cols in the dataset with one-hot vals.
    def one_hot(x, y):
        if type(x) == int or type(x) == float:
            x = str(x)
        try:
            # print(y, x, y in x)
            return y in x
        except:
            return 1==2
    def derive_one_hot(val):
        try:
            assert val not in input_dataframe.columns
        except AssertionError:
            print ('Warning:',val,'is in the features already,you are trying to replace it.')
        iter=[val]*len(input_dataframe)
        # print(len(iter),len(input_dataframe))
        result=pd.Series(map(one_hot,input_dataframe[sel_col[0]],iter),index=input_dataframe.index)
        input_dataframe[val]=result
    map(derive_one_hot,vals)
    return input_dataframe,vals

#Text Extraction
#Get selected information from one col or multiple cols,using regular expression.
def re_extraction(input_dataframe,sel_cols,new_cols,re_method,copy=False):
    '''
    Parameter
        -----
        :param input_dataframe: pd.DataFrame
        :param sel_cols: list,cols to extract from
        :param new_cols: list,new cols
        :param re_method: regularization expression
        :param copy: bool,whether to copy or not
    Return
        -----
        : input_dataframe
    '''
    if copy==True:
        input_dataframe=input_dataframe.copy()
    assert type(sel_cols)==list and type(new_cols)==list
    assert len(sel_cols)==len(new_cols)
    for i in range(len(sel_cols)):
        col=sel_cols[i]
        new_col=new_cols[i]
        # Get index
        index = input_dataframe[col].isnull().values == False
        try:
            # RE extraction
            val_re = input_dataframe[col][index].map(lambda x: re.findall(re_method,x))
            input_dataframe[new_col] = val_re
        except:
            # Report Exceptions
            print('Columns Extraction Warning:',col)
    return input_dataframe

#
# def main():
#     """Main function that is called when datacleaner is run on the command line"""
#     parser = argparse.ArgumentParser(description='A Python tool that automatically cleans data sets and readies them for analysis')
#
#     parser.add_argument('INPUT_FILENAME', type=str, help='File name of the data file to clean')
#
#     parser.add_argument('-cv', action='store', dest='CROSS_VAL_FILENAME', default=None,
#                          type=str, help='File name for the validation data set if performing cross-validation')
#
#     parser.add_argument('-o', action='store', dest='OUTPUT_FILENAME', default=None,
#                         type=str, help='Data file to output the cleaned data set to')
#
#     parser.add_argument('-cvo', action='store', dest='CV_OUTPUT_FILENAME', default=None,
#                         type=str, help='Data file to output the cleaned cross-validation data set to')
#
#     parser.add_argument('-is', action='store', dest='INPUT_SEPARATOR', default='\t',
#                         type=str, help='Column separator for the input file(s) (default: \\t)')
#
#     parser.add_argument('-os', action='store', dest='OUTPUT_SEPARATOR', default='\t',
#                         type=str, help='Column separator for the output file(s) (default: \\t)')
#
#     parser.add_argument('--drop-nans', action='store_true', dest='DROP_NANS', default=False,
#                         help='Drop all rows that have a NaN in any column (default: False)')
#
#     parser.add_argument('--ignore-update-check', action='store_true', dest='IGNORE_UPDATE_CHECK', default=False,
#                         help='Do not check for the latest version of datacleaner (default: False)')
#
#     parser.add_argument('--version', action='version', version='datacleaner v{version}'.format(version=__version__))
#
#     args = parser.parse_args()
#
#     input_data = pd.read_csv(args.INPUT_FILENAME, sep=args.INPUT_SEPARATOR)
#     if args.CROSS_VAL_FILENAME is None:
#         clean_data = autoclean(input_data, drop_nans=args.DROP_NANS, ignore_update_check=args.IGNORE_UPDATE_CHECK)
#         if args.OUTPUT_FILENAME is None:
#             print('Cleaned data set:')
#             print(clean_data)
#             print('')
#             print('If you cannot view the entire data set, output it to a file instead. '
#                   'Type datacleaner --help for more information.')
#         else:
#             clean_data.to_csv(args.OUTPUT_FILENAME, sep=args.OUTPUT_SEPARATOR, index=False)
#     else:
#         if args.OUTPUT_FILENAME is not None and args.CV_OUTPUT_FILENAME is None:
#             print('You must specify both output file names. Type datacleaner --help for more information.')
#             return
#
#         cross_val_data = pd.read_csv(args.CROSS_VAL_FILENAME, sep=args.INPUT_SEPARATOR)
#         clean_training_data, clean_testing_data = autoclean_cv(input_data, cross_val_data,
#                                                                drop_nans=args.DROP_NANS,
#                                                                ignore_update_check=args.IGNORE_UPDATE_CHECK)
#
#         if args.OUTPUT_FILENAME is None:
#             print('Cleaned training data set:')
#             print(clean_training_data)
#             print('')
#             print('Cleaned testing data set:')
#             print(clean_testing_data)
#             print('')
#             print('If you cannot view the entire data set, output it to a file instead. '
#                   'Type datacleaner --help for more information.')
#         else:
#             clean_training_data.to_csv(args.OUTPUT_FILENAME, sep=args.OUTPUT_SEPARATOR, index=False)
#             clean_testing_data.to_csv(args.OUTPUT_FILENAME, sep=args.OUTPUT_SEPARATOR, index=False)
#
# if __name__ == '__main__':
#     main()

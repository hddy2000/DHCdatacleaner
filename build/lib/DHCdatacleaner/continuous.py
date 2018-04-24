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
from utils import replace_value
from sklearn.preprocessing import LabelEncoder
import argparse

# from update_checker import update_check

# from ._version import __version__

# update_checked = False
'''
单数据集清洗的需求：
连续变量
1、missing_value_clean()连续变量：缺失值填补,median,mode...
2、outlier_detect_clean()连续变量：极端值检测/替代outlier/删除
'''
#自动clean实现了两步
# 1、缺失值插补:中位数or众数or前后向补全
def missing_value_clean(input_dataframe, sel_cols,drop_nans=False,method='median', copy=False):
    """Performs a series of automated data cleaning transformations on the provided data set

    Parameters
    ----------
    input_dataframe: pandas.DataFrame
        Data set to clean
    sel_cols:list
        Continuous columns selected
    drop_nans: bool
        Drop all rows that have a NaN in any column (default: False)
    method:string
        method used to fill missing value,could be in {missing,mean,mode,bffill},default median
    copy: bool
        Make a copy of the data set (default: False)
    Returns
    ----------
    output_dataframe: pandas.DataFrame
        Cleaned data set

    """
    # global update_checked
    # if ignore_update_check:
    #     update_checked = True

    # if not update_checked:
    #     update_check('datacleaner', __version__)
    #     update_checked = True
    assert method in {'median','mean','mode','bffill'}

    if copy:
        input_dataframe = input_dataframe.copy()

    if drop_nans:
        print('input N:', len(input_dataframe))
        input_dataframe.dropna(inplace=True)
        print('Done!any case with any missing value in the dataset is excluded.Output N:', len(input_dataframe))
        return input_dataframe

    # if encoder_kwargs is None:
    #     encoder_kwargs = {}

    print('columns to clean:')

    for column in sel_cols:
        print (column)
        # Replace NaNs with the median or mode of the column depending on the column type
        if method=='median':
            input_dataframe[column].fillna(input_dataframe[column].median(), inplace=True)
            print('median fill method is used')
        elif method=='mean':
            input_dataframe[column].fillna(input_dataframe[column].mean(), inplace=True)
            print('mean fill method is used')
        elif method=='mode':
            most_frequent = input_dataframe[column].mode()
            # If the mode can't be computed, use the nearest valid value
            # See https://github.com/rhiever/datacleaner/issues/8
            if len(most_frequent) > 0:
                print('mode fill method is used')
                input_dataframe[column].fillna(input_dataframe[column].mode()[0], inplace=True)
            else:
                print ('No mode is Found')
        elif method=='bffill':
            print('bfill and ffill methods are used')
            input_dataframe[column].fillna(method='bfill', inplace=True)
            input_dataframe[column].fillna(method='ffill', inplace=True)
    print ('Done!')
    return input_dataframe

#连续变量的异常值检测替代,可以批量处理
def outlier_detect_clean(input_dataframe,sel_cols,maxv=None,minv=None,method=None,action='replace',copy=False):
    '''
    Detect all the outlier numbers and replace them using certain method,or delete them.
    Use Median:
    maxv = median + 1.5 * IQR
    minv=  median - 1.5 * IQR
    Use Mean:
    maxv=mean+2*std
    minv=mean-2*std
    All the Outliers will be replaced by these numbers
    
    Parameters
    ---------
    :param input_dataframe: pd.DataFrame
    Data to clean outliers
    :param sel_cols: columns to use, must be continuous
    :param maxv: max value,can be empty if use 'method'
    :param minv: min value,can be empty if use 'method'
    :param method: None,median or mean
    :param action: to delete or replace the outliers,default replace
    :param copy: whether to copy the data or not 
    :return: pd.DataFrame with outliers cleaned with the specific action.
    '''
    if copy:
        input_dataframe=input_dataframe.copy()
    assert method in {None, 'median', 'mean'}
    assert action in {None,'replace','delete'}
    assert type(sel_cols)==list
    for sel_col in sel_cols:
        print(sel_col)
        for u in input_dataframe[sel_col].unique():
            try:
                assert float(u)
            except:
                print (u,'is not continuous in',sel_col)
        median = input_dataframe[sel_col].median()
        IQR = input_dataframe[sel_col].quantile(0.75) - input_dataframe[sel_col].quantile(0.25)
        mean=input_dataframe[sel_col].mean()
        std=input_dataframe[sel_col].std()
        #calculate max and min values using giving methods
        if method=='median':
            maxv = median + 1.5 * IQR
            minv=  median -  1.5*IQR
            print ('range:',maxv,',',minv)
        elif method=='mean':
            maxv=mean+2*std
            minv=mean-2*std
            print ('range:',maxv,',',minv)
        else:
            assert maxv!=None and minv!=None
            print ('No method is specified,use giving arbitrary range.')
            print('range:', maxv, ',', minv)
        values_counts=input_dataframe[sel_col].value_counts()
        #detect outliers
        def f(x):
            return x>maxv
        maxout=list(filter(f,values_counts.index))
        def f(x):
            return x<minv
        minout=list(filter(f,values_counts.index))
        def f(x):
            return x>maxv or x<minv
        ls = list(filter(f, values_counts.index))
        # print (maxout,minout,ls)
        outlier= values_counts[ls]
        print ('outliers detected:')
        print (list(outlier.index))
        print ('Total Outliers:',sum(outlier))
        if action=='replace':
            print (action,'action is conducted')
            #replace outliers
            #replace min
            replace_value(input_dataframe,sel_cols=sel_col,val_list=minout,val_rep=len(minout)*[minv])
            #replace max
            replace_value(input_dataframe, sel_cols=sel_col, val_list=maxout, val_rep=len(maxout) * [maxv])
        elif action=='delete':
            print (action, 'action is conducted')
            # replace min
            replace_value(input_dataframe, sel_cols=sel_col, val_list=minout, val_rep=len(minout) * [np.nan])
            # replace max
            replace_value(input_dataframe, sel_cols=sel_col, val_list=maxout, val_rep=len(maxout) * [np.nan])
            #drop them
            input_dataframe=input_dataframe.ix[input_dataframe[sel_col].dropna().index,:]
        else:
            print ('No action is conducted')
    return input_dataframe



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

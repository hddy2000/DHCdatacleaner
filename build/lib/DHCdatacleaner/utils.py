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
# from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
import argparse
from update_checker import update_check

# from ._version import __version__

update_checked = False
'''
该模块功能：
1、auto_sel_cols():自动识别出连续变量和离散变量的cols
2、replace_value():值替代功能
3、function_derive():采用公式计算该列1对1生成新的col
'''
#自动辨别特征类型
def auto_sel_cols(input_dataframe):
    '''
    Parameter
        -----
        :param input_dataframe:pd.DataFrame 
    
    Return
        ------
        :con_cols:list of col names identified as continuous cols
        :cat_cols:list of col names identified as categorical cols
    '''
    con_cols=[]
    cat_cols=[]
    for column in input_dataframe.columns.values:
        column_type = None
        try:
            map(float,input_dataframe[column].unique())
            column_type=1
        except:
            column_type= 2
        if column_type == 1:
            con_cols.append(column)
        elif column_type == 2:
            cat_cols.append(column)
    print ('continuous:',pd.Series(con_cols))
    print ('categorical:',pd.Series(cat_cols))
    return con_cols,cat_cols
#取值替换，可以批量处理

def replace_value(input_dataframe,sel_cols,val_list,val_rep,copy=False):
    '''
    Parameter
        -----
        :param input_dataframe: pandas.DataFrame
        :param sel_cols: list, selected columns need to replace,
        :param val_list: list,values needs to be replaced,
        :param val_rep:  list,values used to replace,
        :param copy:  copy the data or not,
    Return
        -----
        :input_dataframe:dataframe with value replaced
    '''
    if copy:
        input_dataframe=input_dataframe.copy()
    input_dataframe[sel_cols].replace(val_list, val_rep,inplace=True)
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

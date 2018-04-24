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
from sklearn.preprocessing import LabelEncoder
import argparse
from update_checker import update_check

# from ._version import __version__

update_checked = False
'''
单数据集清洗的需求：
连续
1、连续变量：缺失值填补,median,mode...
2、连续变量：极端值检测和替代outlier
离散
1、离散变量：缺失值填补：forward,backward,model-based,mode...
1、离散变量：one-hot encoding
2、离散变量：one to one encoding
5、离散变量：one to many encoding
6、离散变量：many to one encoding
多数据集的需求：
1、merge需求
2、concate连接需求
3、join的需求
'''
#自动clean实现了两步
# 1、缺失值插补:中位数or众数or前后向补全 2、离散变量自动编码成序号。
def autoclean(input_dataframe, drop_nans=False, copy=False, encoder=None,
              encoder_kwargs=None, ignore_update_check=False):
    """Performs a series of automated data cleaning transformations on the provided data set

    Parameters
    ----------
    input_dataframe: pandas.DataFrame
        Data set to clean
    drop_nans: bool
        Drop all rows that have a NaN in any column (default: False)
    copy: bool
        Make a copy of the data set (default: False)
    encoder: category_encoders transformer
        The a valid category_encoders transformer which is passed an inferred cols list. Default (None: LabelEncoder)
    encoder_kwargs: category_encoders
        The a valid sklearn transformer to encode categorical features. Default (None)
    ignore_update_check: bool
        Do not check for the latest version of datacleaner

    Returns
    ----------
    output_dataframe: pandas.DataFrame
        Cleaned data set

    """
    global update_checked
    if ignore_update_check:
        update_checked = True

    if not update_checked:
        update_check('datacleaner', __version__)
        update_checked = True

    if copy:
        input_dataframe = input_dataframe.copy()

    if drop_nans:
        input_dataframe.dropna(inplace=True)

    if encoder_kwargs is None:
        encoder_kwargs = {}

    print('columns to clean:')

    for column in input_dataframe.columns.values:
        print (column)
        # Replace NaNs with the median or mode of the column depending on the column type
        try:
            input_dataframe[column].fillna(input_dataframe[column].median(), inplace=True)
            print('median fill is used')
        except TypeError:
            most_frequent = input_dataframe[column].mode()
            # If the mode can't be computed, use the nearest valid value
            # See https://github.com/rhiever/datacleaner/issues/8
            if len(most_frequent) > 0:
                print('mode fill is used')
                input_dataframe[column].fillna(input_dataframe[column].mode()[0], inplace=True)
            else:
                print('bfill and ffill is used')
                input_dataframe[column].fillna(method='bfill', inplace=True)
                input_dataframe[column].fillna(method='ffill', inplace=True)

        # Encode all strings with numerical equivalents
        if str(input_dataframe[column].values.dtype) == 'object':
            if encoder is not None:
                print('encoder set by the user is used')
                column_encoder = encoder(**encoder_kwargs).fit(input_dataframe[column].values)
            else:
                print('default encoding method is used')
                column_encoder = LabelEncoder().fit(input_dataframe[column].values)

            input_dataframe[column] = column_encoder.transform(input_dataframe[column].values)
    print ('Done!')
    return input_dataframe
#取值替换，可以批量处理
def replace_value(input_dataframe,sel_cols,val_list,val_rep,copy=False):
    '''
    :param input_dataframe: pandas.DataFrame
    :param sel_cols: list, selected columns need to replace,
    :param val_list: list,values needs to be replaced,
    :param val_rep:  list,values used to replace,
    :param copy:  copy the data or not,
    :return: input_dataframe
    '''
    if copy:
        input_dataframe=input_dataframe.copy()
    input_dataframe[sel_cols] = input_dataframe[sel_cols].replace(val_list, val_rep)
    return input_dataframe
#连续变量的异常值检测替代,可以批量处理
def outlier_detect_replace(input_dataframe,sel_cols,maxv=None,minv=None,method=None,copy=False):
    '''
    Detect all the outlier numbers and replace them with certain method.
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
    :param copy: whether to copy the data or not 
    :return: pd.DataFrame with outliers replaced
    '''
    if copy:
        input_dataframe=input_dataframe.copy()
    assert method in {None, 'median', 'mean'}
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
        outlier={}
        maxout=[]
        minout=[]
        #detect outliers
        for i in values_counts.index:
            if i >maxv:
                # print(i)
                maxout.append(i)
                outlier[i]=values_counts[i]
            if i<minv:
                # print(i)
                minout.append(i)
                outlier[i] = values_counts[i]
        print ('outliers detected:')
        print (outlier.keys())
        print ('Total Outliers:',sum(outlier.values()))
        #replace outliers
        #replace min
        replace_value(input_dataframe,sel_cols=sel_col,val_list=minout,val_rep=len(minout)*[minv])
        #replace max
        replace_value(input_dataframe, sel_cols=sel_col, val_list=maxout, val_rep=len(maxout) * [maxv])
    return input_dataframe

#进行十折交叉试验的清洗
def autoclean_cv(training_dataframe, testing_dataframe, drop_nans=False, copy=False,
                 encoder=None, encoder_kwargs=None, ignore_update_check=False):
    """Performs a series of automated data cleaning transformations on the provided training and testing data sets

    Unlike `autoclean()`, this function takes cross-validation into account by learning the data transformations
    from only the training set, then applying those transformations to both the training and testing set.
    By doing so, this function will prevent information leak from the training set into the testing set.

    Parameters
    ----------
    training_dataframe: pandas.DataFrame
        Training data set
    testing_dataframe: pandas.DataFrame
        Testing data set
    drop_nans: bool
        Drop all rows that have a NaN in any column (default: False)
    copy: bool
        Make a copy of the data set (default: False)
    encoder: category_encoders transformer
        The a valid category_encoders transformer which is passed an inferred cols list. Default (None: LabelEncoder)
    encoder_kwargs: category_encoders
        The a valid sklearn transformer to encode categorical features. Default (None)
    ignore_update_check: bool
        Do not check for the latest version of datacleaner

    Returns
    ----------
    output_training_dataframe: pandas.DataFrame
        Cleaned training data set
    output_testing_dataframe: pandas.DataFrame
        Cleaned testing data set

    """
    global update_checked
    if ignore_update_check:
        update_checked = True

    if not update_checked:
        update_check('datacleaner', __version__)
        update_checked = True

    if set(training_dataframe.columns.values) != set(testing_dataframe.columns.values):
        raise ValueError('The training and testing DataFrames do not have the same columns. '
                         'Make sure that you are providing the same columns.')

    if copy:
        training_dataframe = training_dataframe.copy()
        testing_dataframe = testing_dataframe.copy()
    
    if drop_nans:
        training_dataframe.dropna(inplace=True)
        testing_dataframe.dropna(inplace=True)

    if encoder_kwargs is None:
        encoder_kwargs = {}

    for column in training_dataframe.columns.values:
        # Replace NaNs with the median or mode of the column depending on the column type
        try:
            column_median = training_dataframe[column].median()
            training_dataframe[column].fillna(column_median, inplace=True)
            testing_dataframe[column].fillna(column_median, inplace=True)
        except TypeError:
            column_mode = training_dataframe[column].mode()[0]
            training_dataframe[column].fillna(column_mode, inplace=True)
            testing_dataframe[column].fillna(column_mode, inplace=True)

        # Encode all strings with numerical equivalents
        if str(training_dataframe[column].values.dtype) == 'object':
            if encoder is not None:
                column_encoder = encoder(**encoder_kwargs).fit(training_dataframe[column].values)
            else:
                column_encoder = LabelEncoder().fit(training_dataframe[column].values)

            training_dataframe[column] = column_encoder.transform(training_dataframe[column].values)
            testing_dataframe[column] = column_encoder.transform(testing_dataframe[column].values)

    return training_dataframe, testing_dataframe


def main():
    """Main function that is called when datacleaner is run on the command line"""
    parser = argparse.ArgumentParser(description='A Python tool that automatically cleans data sets and readies them for analysis')

    parser.add_argument('INPUT_FILENAME', type=str, help='File name of the data file to clean')

    parser.add_argument('-cv', action='store', dest='CROSS_VAL_FILENAME', default=None,
                         type=str, help='File name for the validation data set if performing cross-validation')

    parser.add_argument('-o', action='store', dest='OUTPUT_FILENAME', default=None,
                        type=str, help='Data file to output the cleaned data set to')

    parser.add_argument('-cvo', action='store', dest='CV_OUTPUT_FILENAME', default=None,
                        type=str, help='Data file to output the cleaned cross-validation data set to')

    parser.add_argument('-is', action='store', dest='INPUT_SEPARATOR', default='\t',
                        type=str, help='Column separator for the input file(s) (default: \\t)')
                    
    parser.add_argument('-os', action='store', dest='OUTPUT_SEPARATOR', default='\t',
                        type=str, help='Column separator for the output file(s) (default: \\t)')

    parser.add_argument('--drop-nans', action='store_true', dest='DROP_NANS', default=False,
                        help='Drop all rows that have a NaN in any column (default: False)')
                        
    parser.add_argument('--ignore-update-check', action='store_true', dest='IGNORE_UPDATE_CHECK', default=False,
                        help='Do not check for the latest version of datacleaner (default: False)')

    parser.add_argument('--version', action='version', version='datacleaner v{version}'.format(version=__version__))

    args = parser.parse_args()

    input_data = pd.read_csv(args.INPUT_FILENAME, sep=args.INPUT_SEPARATOR)
    if args.CROSS_VAL_FILENAME is None:
        clean_data = autoclean(input_data, drop_nans=args.DROP_NANS, ignore_update_check=args.IGNORE_UPDATE_CHECK)
        if args.OUTPUT_FILENAME is None:
            print('Cleaned data set:')
            print(clean_data)
            print('')
            print('If you cannot view the entire data set, output it to a file instead. '
                  'Type datacleaner --help for more information.')
        else:
            clean_data.to_csv(args.OUTPUT_FILENAME, sep=args.OUTPUT_SEPARATOR, index=False)
    else:
        if args.OUTPUT_FILENAME is not None and args.CV_OUTPUT_FILENAME is None:
            print('You must specify both output file names. Type datacleaner --help for more information.')
            return
    
        cross_val_data = pd.read_csv(args.CROSS_VAL_FILENAME, sep=args.INPUT_SEPARATOR)
        clean_training_data, clean_testing_data = autoclean_cv(input_data, cross_val_data,
                                                               drop_nans=args.DROP_NANS,
                                                               ignore_update_check=args.IGNORE_UPDATE_CHECK)

        if args.OUTPUT_FILENAME is None:
            print('Cleaned training data set:')
            print(clean_training_data)
            print('')
            print('Cleaned testing data set:')
            print(clean_testing_data)
            print('')
            print('If you cannot view the entire data set, output it to a file instead. '
                  'Type datacleaner --help for more information.')
        else:
            clean_training_data.to_csv(args.OUTPUT_FILENAME, sep=args.OUTPUT_SEPARATOR, index=False)
            clean_testing_data.to_csv(args.OUTPUT_FILENAME, sep=args.OUTPUT_SEPARATOR, index=False)

if __name__ == '__main__':
    main()

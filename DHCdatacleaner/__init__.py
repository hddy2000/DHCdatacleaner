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

0.1.0 Version
0.1.0版本功能
UTILS：
1、auto_sel_cols():
Automatically Select the continuous and catigorical columns for you.
自动识别出连续变量和离散变量的cols
2、replace_value() 
Replace specific values.
值替代功能

CONTINUOUS：
1、missing_value_clean()
To delete the missing cases,or imputate them.
连续变量：缺失值填补,median,mean,mode,bfill+ffill(前后向插补)等办法
2、outlier_detect_clean()
To detect the outlier and replace them by the method you specified,or just delete them.
连续变量：使用给定的方法(median、mean或自定义),将极端值检测和替代outlier,或删除outlier。

CATEGORICAL：
1、missing_value_clean() 
To delete the missing cases,or imputate them.
离散变量：缺失值填补,mode,bfill+ffill(前后向插补)等办法
2、word_num_encode() 
To Label word into numbers
离散变量：从文字到数字的encoding


TRANSFORM:
1、function_derive() 
Use a function to create derived cols.
利用给定函数1对1衍生新的列
2、one_hot_transform()
特征变换：one-hot encoding
该离散变量中所有的值，内容都为单一词组，或者用逗号等符号分割，可将每个词组都提升为一个单一特征（升维）。
3、re_extraction()
Use regularization expression to extract information,the returned col values will be list type
用正则表达式提取内容，提取出来的内容是返回list

Under Construction 待完成：
1、离散变量：many cols to one col encoding

请使用help（）看每个模块详解
For more details please see help() for each module.
欢迎提出宝贵意见和建议！
Questions and advices are welcome!
"""

from ._version import __version__
import utils
import categorical
import continuous
import transform
from utils import auto_sel_cols,replace_value
from transform import function_derive, one_hot_derive,re_extraction

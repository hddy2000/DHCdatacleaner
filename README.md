# DHCdatacleaner
Easy Data Clean Modules from DHC!
安装说明：
1、请从Terminal进入该文件夹所在的文件路径：比如C:/DHCdatacleaner。
2、输入命令 python setup.py install。
3、进入你要编辑的Jupiter notebook或者py文件，import DHCdatacleaner就可以用了。
4、可以用help()命令看各个模块功能参数介绍。

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

Under Construction 待完成：
1、离散变量：many cols to one col encoding

请使用help（）看每个模块详解
For more details please see help() for each module.
欢迎提出宝贵意见和建议！
Questions and advices are welcome!

### 简述
* 本项目适用于Android本地化开发，将java代码和xml中的中文统一整理到string.xml，并替换原文本。

### 背景
* 由于项目开发的不规范，赶进度等各种为所欲为的操作，导致项目庞大后再做本地化变得繁琐，枯燥，机械化。目前手中两个项目，其中一个已经几年了，初步统计在代码和xml中的中文超过了2000+处，让人惶恐。于是本着能用程序解决的问题绝不动手的原则，想通过python来完成替换和整理的工作。

### 原理
* 先查找string.xml中已经存在的中文
* 遍历所有的文件，文件的每一行
* 如果有包含中文的字符串就与string.xml中的作比较
* 如果存在，就直接替换此处文本
    * 如果是Java文件
        * 如果是Activity或Fragment就直接使用getString(R.string.xxx)来替换
        * 如果不是，就使用ApplicationContext.getString(R.string.xxx)来替换
    * 如果是xml文件，直接使用@string/xxx来替换
* 如果不存在，就把包含中文的字符串写入string.xml，然后再进行替换
    * 自动生成string的name
        * 取字符串前4个字转拼音，在结尾加上三个随机串
    * 手动输入string的name
        * 手动输入需要的name
* 在写入的时候会维护一个list保存当前string.xml中已有的字符串，避免遍历的时候重复写入
* 如此循环，直到结束

### 说明
#### 使用说明
* 文件路径
    * xml_path = '/XXX/app/src/main/res/values/strings.xml'【项目中strings.xml的绝对路径】
    * main_path = '/XXX/app/src/main'【项目的绝对路径】
    * app_context = 'XXX.getInstance().'【项目中全局APPlicationContext】
* 成效 
    * 10W行代码的项目大概2分钟能完成替换
    * 加上手动修改，1天即可完成本地化
#### 注意事项
* 特殊字符处理
    * 字符串存在各种符号，html代码等情况，需要手动处理
* 全局中文问题
    * 文字在全局变量，ApplicationContext可能为空，需要注意
* 导入ApplicationContext
    * 替换的时候没有导入ApplicationContext包，需要手动添加

### 待扩展
#### 数字打头/特殊字符
* 可以只提取其中的中文来转拼音，如果没有中文就直接添加随机字符串 
#### html代码
* 有包含html代码的字符串，直接跳过替换
#### 全局变量的中文
* 整合到统一的文件，方便管理
#### Kotlin

#### 导入头文件
* 在使用ApplicationContext.getString(R.string.xxx)的时候导入ApplicationContext的包
### 写在最后
* 欢迎大家来拍砖，来扩展

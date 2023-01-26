# Python课程设计&KVM课程设计

## 说明

本项目包含南阳理工学院2021年6月《Python程序开发》与《KVM虚拟化实践与编程》科目课程设计
Python程序设计：简单汽车销售管理
KVM虚拟化实践与编程：云平台管理系统

## Python程序设计

简单汽车销售管理：基于Python语言，使用guietta实现用户界面，将表格生成输出成为图片

#### 实验要求

以下内容来自于《Python课程设计任务书》

    基本要求： 
    1）复习并深入理解Python语言基本特性、数据文件读取方法及面向对象思想；
    2）掌握Python语言相关特性，熟悉相关常用函数的使用；
    3）研究并掌握Python面向对象的语法特点和使用方法；

    问题描述（功能要求）： 
    根据实验指导书要求，完成相关软件系统的设计，要求内容翔实，条理清晰，主要（关键代码）须有详细注释，写清楚测试结果，并分析存在的问题：
    1）能够实现汽车销售管理与相关信息的保存（到文件）和读取；
    2）实现所有库存汽车相关信息的录入、显示、销售、修改等功能；
    3）系统界面应类似下图所示的控制台界面（鼓励使用WEB或桌面窗体界面）

## KVM虚拟化实践与编程

使用 Python 语言制作了一个云平台管理系统。在时限内完成了这个系统的虚拟机管理功能，即虚拟机的创建、删除、启动、暂停、恢复等功能。

#### 实现功能

此系统所实现的功能：
1） 虚拟机的创建与删除。
可以从现有的 img 文件或者 iso 文件进行虚拟机的添加。
2） 虚拟机的管理
包括启动、关闭、暂停、恢复以及查看列表等常用功能。
3） 网络设置
包含 network、bridge 等网络参数写入 xml 文件中
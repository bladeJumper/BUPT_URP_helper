# BUPT_URP_helper
北邮选课助手

Features
--------------

* OCR识别验证码自动登陆
* 输入课程序号进行课程查找和选课
* 挂机抢课
* 自定义选课尝试间隔
* 自定义选课尝试次数

Requirements
--------------
* Python 3+
* python依赖：pytesseract, PIL
* 非python依赖：tesseract https://github.com/tesseract-ocr/tesseract

Usage:
---------------

* 在URP-helper.py文件中输入你的学号和教务系统密码

![账号信息填写](https://github.com/XieZhuoJun/BUPT_URP_helper/blob/master/resource/%E6%89%B9%E6%B3%A8%202019-07-08%20010519.png)
* 在教务系统下载课程信息后输入URP-helper.py


![选课信息填写](https://github.com/XieZhuoJun/BUPT_URP_helper/blob/master/resource/%E6%89%B9%E6%B3%A8%202019-07-08%20011433.png)

kcid: 课程id + 下划线 + 课程序号

kcty: 课程类型 (方案课程（2）、系任选课（4）、校任选课（3）)

success: 成功标记列表，要选多少门课就填几个0 (To be improved but I`m lazy)

可以一次填入多门课程，示例：

  kcid = ["3132114070_01","2122114270_01"]

  kcty = ["2","2"]

  kcty = [0,0]
  
maxloop: 最大尝试次数，0代表无限

sleeptime: 尝试间隔，单位秒(s)

* 命令行输入：python URP_helper.py 开始选课！

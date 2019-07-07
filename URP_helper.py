# -*- coding: UTF-8 -*-

import requests
import time
from PIL import Image,ImageEnhance
import pytesseract
import urllib3

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

#登陆数据头部，在这里输入你的学号和密码，POST登陆请求时程序将自动在尾部加入验证码形成完整的POST数据
dataheader = "type=sso&zjh=********&mm=********&v_yzm="
#教务系统主机ip
host = "10.3.255.178"
#选课信息
kcid = ["3132114070_01"]
kcty = ["2"]
success = [0]
maxloop = 0
sleeptime= 0.1
#验证码识别
def image_to_str(path):
    image = Image.open(path)
    image = image.convert('L')
    vcode = pytesseract.image_to_string(image)
    return vcode

#登陆教务系统的函数，登陆成功则返回cookies中"JSESSIONID"的值，失败则返回'0'
def login():
    
    #用GET方法访问教务系统登陆界面，获取验证码和COOKIES信息
    valcode = requests.get('https://jwxt.bupt.edu.cn/validateCodeAction.do?random=',verify=True)
    cookies = valcode.cookies
    
    #验证码的保存和识别
    file = open('vcode.jpg','wb')
    file.write(valcode.content)
    file.close()
    vcode = image_to_str('vcode.jpg')
    '''
    #手工输入验证码
    #image = Image.open('vcode.jpg')
    #image.show()
    #vcode = input("VCODE:")
    '''
    print("尝试验证码：",vcode)
    
    #组装数据体
    data = dataheader + vcode
    
    #数据头部
    headers = {"Connection":"keep-alive",
        "Content-Length":"47",
        "Cache-Control":"max-age=0",
        "Origin":"https://jwxt.bupt.edu.cn",
        "Upgrade-Insecure-Requests":"1",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"https://jwxt.bupt.edu.cn/",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }

    #发送登陆信息，并将返回值保存
    response = requests.post('https://jwxt.bupt.edu.cn/jwLoginAction.do', headers = headers, cookies = cookies, data = data)
    #index = requests.get(acturl, headers = headers, cookies = cookies)

    #print(cookies.get("JSESSIONID"))
    #登陆成功的校验字符
    chk = "学分制综合教务"
    #判断登陆是否成功
    if(chk in response.text):
        return cookies.get("JSESSIONID")
    else:
        return '0'

#跳转至选课界面
def jump(cookies):
    headers = {"Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"https://jwxt.bupt.edu.cn/menu/s_menu.jsp",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }
    res = requests.get('https://jwxt.bupt.edu.cn/xkAction.do?actionType=-1', headers = headers, cookies = cookies)
    #跳转成功，返回1
    chk = "课程"
    if(chk in res.text):
        return 1
    else:
        return 0

#跳转到课程信息界面
def coursedata(kcid,kcty,cookies):
    headers = {"Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"https://jwxt.bupt.edu.cn/xkAction.do?actionType=-1",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }
    page = 2
    url = "https://jwxt.bupt.edu.cn/xkAction.do?actionType="+kcty+"&pageNumber="+str(page)+"&oper1=ori"
    res = requests.get(url, headers = headers, cookies = cookies)
    '''
    #检查是否找到课程
    chk = kcid[0:9]
    inchk = "课程"
    while(page<11):
        if(chk in res.text):
            return str(page)
        else:
            if(inchk in res.text):
                print("未找到目标课程，跳转到下一页")
                page = page + 1
                loopcount = 1
            url = "http://10.3.255.178/xkAction.do?actionType="+kcty+"&pageNumber="+str(page)+"&oper1=ori"
            print("在第",page,"页进行本页第",loopcount,"次查询")
            res = requests.get(url, headers = headers, cookies = cookies)
            loopcount = loopcount + 1
        if(loopcount > 1000):
            print("课程查询失败")
            return "-1"
        time.sleep(0.1)
    return "-1"
    '''
    chk = "2016"
    if chk in res.text:
        return 1
    else:
        return 0

#选课中间函数,参数为课程id，课程种类（方案课程（2）、系任选课（4）、校任选课（3）），课程所在页数,cookies
def xk(kcid,coursetype,page,cookies):
    #选课
    headers = {"Connection":"keep-alive",
        "Content-Length":"47",
        "Cache-Control":"max-age=0",
        "Origin":"http://10.3.255.178",
        "Upgrade-Insecure-Requests":"1",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"https://jwxt.bupt.edu.cn/xkAction.do?actionType="+coursetype+"&pageNumber="+page+"&oper1=ori",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }
    data = {"kcId":kcid,
        "preActionType":"2",
        "actionType":"9"}

    response = requests.post('https://jwxt.bupt.edu.cn/xkAction.do', headers = headers, cookies = cookies, data = data)
    succchk = "成功"
    nologchk = "初始化函数"
    if succchk in response.text:
        return 1
    elif nologchk in response.text:
        return -1
    else:
        return 0

#课程输入，若没有找到且选择放弃选课，则return -1，其他情况return正整数，默认return 1
#已不需要，无需搜索到课程也可以选课
def search(kcid,kcty,cookies):
    pages = coursedata(kcid,kcty,cookies)
    while(pages == '-1'):
        print("未找到课程")
        select = input("是否重试？y/n: ")
        if(select == 'y'):
            select = input("是否重新输入课程信息？y/n: ")
            if(select == 'y'):
                kcid = input("请输入课程id_课程序号 例：3412110160_01\n")
                kcty = input("请输入课程类型，方案课程（2）、系任选课（4）、校任选课（3）\n")
            pages = coursedata(kcid,kcty,cookies)
        else:
            print("放弃寻找\n")
            print("放弃选课，准备注销")
            logout(cookies)
            return -1
    print("在第",pages,"页找到课程，开始选课")
    return pages

#注销
def logout(cookies):
    
    headers = {"Connection":"keep-alive",
        "Content-Length":"47",
        "Cache-Control":"max-age=0",
        "Origin":"https://jwxt.bupt.edu.cn/",
        "Upgrade-Insecure-Requests":"1",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"https://jwxt.bupt.edu.cn/menu/s_top.jsp",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }

    data = {"loginType":"jwLogin"}
    logout = requests.post('https://jwxt.bupt.edu.cn/logout.do',headers = headers , cookies = cookies, data = data)
    print("注销成功！")

def trylogin():
    loopcount = 1
    jsessionid = '0'
    print("登陆信息",dataheader)
    while(jsessionid=='0'):
        print("尝试第",loopcount,"次登陆")
        try:
            jsessionid = login()
        except e:
            print(e)
            loopcount = loopcount
        loopcount = loopcount + 1
        if(loopcount == 22):
            print("登陆失败，请检查登陆信息和网络连接状态")
            return '0'
        time.sleep(1)
    cookies = {"JSESSIONID":jsessionid}
    print("登陆成功，准备进行选课")
    return cookies

def tryjump(cookies):
    chk = 0
    loopcount = 1
    select = []
    while(chk == 0):
        print("尝试第",loopcount,"次跳转至选课方案页面")
        chk = jump(cookies)
        loopcount = loopcount + 1
        if(loopcount == 1000):
            print("跳转失败，网络错误或服务器压力过大")
            select = input("是否重试？y/n: ")
            if(select == 'y'):
                loopcount = 1
            else:
                return 0
        time.sleep(0.1)
    print("跳转成功！")

def trycoursedata(kcid,kcty,cookies):
    chk = 0
    loopcount = 1
    select = []
    while(chk == 0):
        print("尝试第",loopcount,"次跳转至课程信息页面,课程类型(方案课程（2）、系任选课（4）、校任选课（3）)：",kcty)
        chk = coursedata(kcid,kcty,cookies)
        loopcount = loopcount + 1
        if(loopcount == 1000):
            print("跳转失败，网络错误或服务器压力过大")
            select = input("是否重试？y/n: ")
            if(select == 'y'):
                loopcount = 1
            else:
                return 0
        time.sleep(0.1)
    print("跳转成功！")

#主函数
def xktest():
    cookies = trylogin()
    #kcid = input("请输入课程id_课程序号 例：3412110160_01\n")
    #kcty = input("请输入课程类型，方案课程（2）、系任选课（4）、校任选课（3）\n")
    #maxloop = int(input("请输入最大抢课次数\n"))
    #sleeptime = float(input("请输入两次抢课的间隔（s）\n"))
    print("课程id",kcid,"课程类别",kcty,"最大尝试次数",maxloop)
    print("(方案课程（2）、系任选课（4）、校任选课（3）)")
    input("按任意键开始选课")    
    
    #跳转到选课方案界面
    tryjump(cookies)
    prevty = "-1"
    #选课
    remain = len(kcid)
    loopcount = 0
    while(remain!=0 and (loopcount != maxloop or maxloop==0)):
        chk = 0
        loopcount = loopcount+1
        print("第",loopcount,"/",maxloop,"次尝试,已选",len(kcid)-remain,"门,剩余",remain,"门",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        for i in range(len(kcid)):
            if(success[i]==0):
                if(prevty != kcty[i]):
                    #跳转至课程信息页面
                    trycoursedata(kcid[i],kcty[i],cookies)
                    prevty = kcty[i]
                chk = xk(kcid[i],kcty[i],"1",cookies)
            if(chk==1):
                print("成功选取：",kcid[i])
                success[i]==1
                remain = remain-1
            
            elif chk==-1:   #检测到掉线
                print("检测到掉线，尝试重新登陆")
                cookies = trylogin()#重新登陆
                tryjump(cookies)    #跳转至选课方案页面
                prevty = "-1"       #重置选课信息页面
        if(loopcount==maxloop):
            sel = input("达到最大尝试次数，是否继续？y/n")
            if(sel == 'y'):
                loopcount = 0
        time.sleep(sleeptime)
    print("选课结束，准备注销")
    logout(cookies)
    return 0
xktest()

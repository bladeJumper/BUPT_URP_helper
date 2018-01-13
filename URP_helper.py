import requests
import chkchar
import time
import bs4
from PIL import Image

#登陆数据头部，在这里输入你的用户名和密码，POST登陆请求时程序将自动在尾部加入验证码形成完整的POST数据
dataheader = "type=sso&zjh=用户名&mm=密码&v_yzm="

#登陆教务系统的函数，登陆成功则返回cookies中"JSESSIONID"的值，失败则返回'0'
def login():
    
    #用GET方法访问教务系统登陆界面，获取验证码和COOKIES信息
    valcode = requests.get('http://jwxt.bupt.edu.cn/validateCodeAction.do?random=')
    cookies = valcode.cookies
    
    #验证码的保存和识别
    file = open('vcode.jpg','wb')
    file.write(valcode.content)
    file.close()
    vcode = chkchar.image_to_str('vcode.jpg')
    print("尝试验证码：",vcode)
    
    #组装数据体
    data = dataheader + vcode
    
    #数据头部
    headers = {"Connection":"keep-alive",
        "Content-Length":"47",
        "Cache-Control":"max-age=0",
        "Origin":"http://jwxt.bupt.edu.cn",
        "Upgrade-Insecure-Requests":"1",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"http://jwxt.bupt.edu.cn/",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }

    #发送登陆信息，并将返回值保存
    response = requests.post('http://jwxt.bupt.edu.cn/jwLoginAction.do', headers = headers, cookies = cookies, data = data)
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
        "Referer":"http://jwxt.bupt.edu.cn/menu/s_main.jsp",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }
    res = requests.get('http://jwxt.bupt.edu.cn/xkAction.do?actionType=-1', headers = headers, cookies = cookies)
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
        "Referer":"http://jwxt.bupt.edu.cn/xkAction.do?actionType=-1",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }
    page = 1
    url = "http://jwxt.bupt.edu.cn/xkAction.do?actionType="+kcty+"&pageNumber="+str(page)+"&oper1=ori"
    res = requests.get(url, headers = headers, cookies = cookies)
    chk = kcid[0:9]
    inchk = "课程"
    while(page<11):
        if(chk in res.text):
            return str(page)
        else:
            if(inchk in res.text):
                page = page + 1
            url = "http://jwxt.bupt.edu.cn/xkAction.do?actionType="+kcty+"&pageNumber="+str(page)+"&oper1=ori"
            res = requests.get(url, headers = headers, cookies = cookies)

    return "-1"



#选课中间函数,参数为课程id，课程种类（方案课程（2）、系任选课（4）、校任选课（3）），课程所在页数,cookies
def xk(kcid,coursetype,page,cookies):
    #选课
    headers = {"Connection":"keep-alive",
        "Content-Length":"47",
        "Cache-Control":"max-age=0",
        "Origin":"http://jwxt.bupt.edu.cn",
        "Upgrade-Insecure-Requests":"1",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"http://jwxt.bupt.edu.cn/xkAction.do?actionType="+coursetype+"&pageNumber="+page+"&oper1=ori",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }
    data = {"kcId":kcid,
        "preActionType":"2",
        "actionType":"9"}

    response = requests.post('http://jwxt.bupt.edu.cn/xkAction.do', headers = headers, cookies = cookies, data = data)
    faichk = "对不起"
    succchk = "成功"
    if faichk in response.text:
        return 0
    elif succchk in response.text:
        return 1
    else:
        return -1

#注销
def logout(cookies):
    
    headers = {"Connection":"keep-alive",
        "Content-Length":"47",
        "Cache-Control":"max-age=0",
        "Origin":"http://jwxt.bupt.edu.cn",
        "Upgrade-Insecure-Requests":"1",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"http://jwxt.bupt.edu.cn/menu/s_top.jsp",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }

    data = {"loginType":"jwLogin"}
    logout = requests.post('http://jwxt.bupt.edu.cn/logout.do',headers = headers , cookies = cookies, data = data)
    print("注销成功！")

#主函数
def xktest():
    loopcount = 1
    jsessionid = '0'
    while(jsessionid=='0'):
        print("尝试第",loopcount,"次登陆")
        try:
            jsessionid = login()
        except:
            loopcount = loopcount
        loopcount = loopcount + 1
        if(loopcount == 21):
            print("登陆失败，请检查登陆信息和网络连接状态")
            return '0'
        time.sleep(0.2)

    cookies = {"JSESSIONID":jsessionid}
    print("登陆成功，准备进行选课")


    #跳转到选课方案界面
    chk = 0
    loopcount = 1
    while(chk == 0):
        print("尝试第",loopcount,"次跳转至选课方案页面")
        chk = jump(cookies)
        print(chk)
        loopcount = loopcount + 1
        if(loopcount == 1000):
            print("跳转失败，网络错误或服务器压力过大")
            return 0
        time.sleep(0.2)
    print("跳转成功！")

    kcid = []
    kcty = []
    kcid = input("请输入课程id_课程序号 例：3412110160_01\n")
    kcty = input("请输入课程类型，方案课程（2）、系任选课（4）、校任选课（3）\n")
    input("按任意键开始选课")
    print("开始寻找课程")
    #跳转到课程信息界面
    pages = coursedata(kcid,kcty,cookies)
    if(pages == '-1'):
        print("未找到课程")
    else:
        print("在第",pages,"页找到课程，开始选课")

    loopcount = 1
    while(loopcount < 1000):
        succhk = xk(kcid,kcty,pages,cookies)
        print("第",loopcount,"次尝试")
        if(succhk == 1):
            print("选课成功！")
            break
        elif(succhk == 0):
            print("课程时间冲突或已达到最大可选课程数！")
        else:
            print("其他错误")
        loopcount = loopcount + 1
        time.sleep(1)
    logout(cookies)
xktest()
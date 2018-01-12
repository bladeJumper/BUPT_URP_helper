import requests
import time
import chkchar
from PIL import Image

logurl = 'http://jwxt.bupt.edu.cn/jwLoginAction.do'
acturl = 'http://jwxt.bupt.edu.cn/'
vcodeurl = 'http://jwxt.bupt.edu.cn/validateCodeAction.do?random='

#数据头部，zjh和mm对应学号和教务系统密码，POST登陆请求时程序将自动在尾部加入验证码形成完整的POST数据
dataheader = "type=sso&zjh=在此处填入学号&mm=在此处填入密码&v_yzm="

#登陆教务系统的函数，登陆成功则返回cookies中"JSESSIONID"的值，失败则返回'0'
def login():
    
    #用GET方法访问教务系统登陆界面，获取验证码和COOKIES信息
    valcode = requests.get(vcodeurl)
    cookies = valcode.cookies
    
    #验证码的保存和识别
    file = open('vcode.jpg','wb')
    file.write(valcode.content)
    file.close()
    vcode = chkchar.image_to_str('E:\\raspberryPi\\ocr\\vcode.jpg')
    
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
    response = requests.post(logurl, headers = headers, cookies = cookies, data = data)
    #index = requests.get(acturl, headers = headers, cookies = cookies)

    #print(cookies.get("JSESSIONID"))
    
    #登陆成功的校验字符
    chk = "学分制综合教务"
    #判断登陆是否成功
    if(chk in response.text):
        return cookies.get("JSESSIONID")
    else:
        return '0'

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
        time.sleep(0.1)

    cookies = {"JSESSIONID":jsessionid}
    print("登陆成功，准备进行选课")

    #"Referer":"http://jwxt.bupt.edu.cn/menu/s_menu.jsp",
    #跳转到选课界面
    headers = {"Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"http://jwxt.bupt.edu.cn/menu/s_main.jsp",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }
    requests.get('http://jwxt.bupt.edu.cn/xkAction.do?actionType=-1', headers = headers, cookies = cookies)

    headers = {"Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"http://jwxt.bupt.edu.cn/xkAction.do?actionType=-1",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }

    coursedata = requests.get('http://jwxt.bupt.edu.cn/xkAction.do?actionType=2&pageNumber=-1&oper1=ori',headers = headers, cookies = cookies)
    #print(coursedata.text)

    #选课
    headers = {"Connection":"keep-alive",
        "Content-Length":"47",
        "Cache-Control":"max-age=0",
        "Origin":"http://jwxt.bupt.edu.cn",
        "Upgrade-Insecure-Requests":"1",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer":"http://jwxt.bupt.edu.cn/xkAction.do?actionType=2&pageNumber=-1&oper1=ori",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5",
    }

    data = {"kcId":"3412110160_01",
        "preActionType":"2",
        "actionType":"9"}
    
    response = requests.post('http://jwxt.bupt.edu.cn/xkAction.do', headers = headers, cookies = cookies, data = data)
    print(response.text)

    #注销
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
xktest()
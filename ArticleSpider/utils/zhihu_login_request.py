import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
header = {
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com/",
    "User-Agent":agent
}
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")

try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")

def is_login():
    inbox_url = "http://www.zhihu.com/inbox"
    response = session.get(inbox_url,headers=header,allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def get_xsrf():
    #获取xsrf code
    response = session.get("https://www.zhihu.com", headers=header)
    # print(response.text)
    match_obj = re.search('.*<input type="hidden" name="_xsrf" value="(.*?)"', response.text)
    # print(match_obj.group(1))
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""

# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=header)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码<font></font>
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入<font></font>
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha

def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html","wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


def zhihu_login(account,password):
    # 知乎登陆
    if re.match("^1\d{10}",account):
        print("手机号码登陆")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf" : get_xsrf(),
            "photo_num" : account,
            "password": password,
            'remember_me': 'true',
            "captcha": ""
        }

    else:
        if "@" in account:
            print("邮箱登陆")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password,
                'remember_me': 'true',
                "captcha": ""
            }
    # 不需要验证码
    # response_text = session.post(post_url, post_data, headers=header)
    # session.cookies.save()

    post_data["captcha"] = get_captcha()
    login_page = session.post(post_url, data=post_data, headers=header)
    login_code = eval(login_page.text)
    print(login_code['msg'])
    session.cookies.save("zhihu_cookie.txt")

zhihu_login('','')
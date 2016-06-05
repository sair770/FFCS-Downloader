from PIL import Image
import mechanize,cookielib
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from StringIO import StringIO
import json, timeit,os
from CaptchaParser import CaptchaParser
import urllib2, urllib
from cookielib import CookieJar

# input-type values from the html form

def login():
    if os.path.isfile('cre.json'):
        with open('cre.json', 'r') as f:
            data = json.load(f)
            regno = data['username']
            passw = data['password']

    else:
        regno=raw_input("Registration Number: ")
        passw=raw_input("Password: ")
        with open('cre.json', 'w') as f:
            f.write(json.dumps({
                'username': regno,
                'password': passw
            }, ensure_ascii=False))
            f.close()
    
    cj = cookielib.CookieJar()
    br= mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_cookiejar(cj)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))


    print "Fetching Captcha"
    r=br.open('https://vtop.vit.ac.in/student/stud_login.asp')
    html=r.read()
    soup=BeautifulSoup(html)
    im = soup.find('img', id='imgCaptcha')
    image_response = br.open_novisit(im['src'])
    img=Image.open(StringIO(image_response.read()))
    imgcpy=img.copy()
    starttime = timeit.default_timer()
    parser=CaptchaParser()
    captcha=parser.getCaptcha(img)
    stoptime = timeit.default_timer()

    print "Recognized Captcha:"+str(captcha)+" in "+str(stoptime-starttime)
    formdata = { "regno" : regno, "passwd": passw, "vrfcd" : str(captcha) }
    data_encoded = urllib.urlencode(formdata)
    response = opener.open('https://vtop.vit.ac.in/student/stud_login_submit.asp', data_encoded)


    print "Logging in User:"+str(regno)

    print response.geturl()

    if(response.geturl()=="https://vtop.vit.ac.in/student/home.asp"):
	    print"Success!"

    else:
	    print '''Failed :(
                 Either Username or Password is wrong or there is some fault in decoding captcha try again'''
     
    return opener
    
if __name__=="__main__":
    
    br=login()
    
import sys
import re
from helper import login
from BeautifulSoup import BeautifulSoup as bs
import time
import os
import urllib2
import urllib
user_id = ''
passw = ''
#print cj
baseurl='https://vtop.vit.ac.in/student/'
timtable='/timetable_ss.asp'
attendance='/attn_report.asp?sem=SS&fmdt=%s&todt=%s'
crpg='/coursepage_view.asp?sem=SS&crs=%s&slt=%s&fac=%s'
facid='https://vtop.vit.ac.in/student/getfacdet.asp?fac=%s'
list_subject=[]
empid=[]
req=[0,1,2,7,8,9]

def ask():
    print '''

  **********    **********       *****     *****                                          
  *             *              *          *                                       
  *             *             *           *                                        
  ******        ******        *            *****                                                
  *             *             *                 *                                  
  *             *              *                *                                
  *             *                *****     *****  '''  
    print '\n\n'
    print '''
    Select semester
    [1] Summer
    [2] Winter
    [3] Fall'''
    i = int(raw_input('Enter your choice: '))
    global timtable
    global attendance
    global crpg
    time_table=['/timetable_ss.asp','/timetable_ws.asp','/timetable_fs.asp']
    attendance_list=['/attn_report.asp?sem=SS&fmdt=%s&todt=%s','/attn_report.asp?sem=WS&fmdt=%s&todt=%s','/attn_report.asp?sem=FS&fmdt=%s&todt=%s']
    crpg_list=['/coursepage_view.asp?sem=SS&crs=%s&slt=%s&fac=%s','/coursepage_view.asp?sem=WS&crs=%s&slt=%s&fac=%s','/coursepage_view.asp?sem=FS&crs=%s&slt=%s&fac=%s']
    timtable = time_table[i-1]
    attendance = attendance_list[i-1]
    crpg = crpg_list[i-1]
    

def createfold(slot,fac):
    d=os.environ['USERPROFILE']+'\\Downloads'
    if os.path.exists(d+'\\'+slot+'\\'+fac):
        p = d+'\\'+slot+'\\'+fac
    else:
        try:
            if os.path.exists(d+'\\'+slot):
                os.mkdir(d+'\\'+slot+'\\'+fac)
            else:
                os.mkdir(d+'\\'+slot)
                os.mkdir(d+'\\'+slot+'\\'+fac)
            p = d+'\\'+slot+'\\'+fac
        except:
            try:
                os.mkdir(d+'\\'+fac)
                p=d+'\\'+fac
            except:    
                print "Not able to able to make folder"
                sys.exit(0)
                pass            
    return p

'''
Example of metadata
1.pptx
Cache-Control: private
Content-Length: 2672781
Content-Type: application/octet-stream
Server: Microsoft-IIS/7.5
Content-Disposition: attachment;Filename=SUMSEM2015-16_CP0158_27-MAY-2016_RM01_1
.pptx
X-Powered-By: ASP.NET
Date: Sun, 05 Jun 2016 11:01:36 GMT
Connection: close
'''

def down(url, file_nam, path_folder):
    date=re.compile(r"([0-9]{2,2}[-]+[A-Z]+[a-z]{2,2}[-]+[0-9]{4,4})")
    da=date.search(url)
    ex=url.split('.')
    if da:
        da=da.group() 
        da=da.split('-')
        da=da[1]+'-'+da[0]+'-'+da[2]+'-'
    try:
        u = br.open(baseurl+"/"+url)
        meta_data = u.info()
        file_size = int(meta_data.getheaders("Content-Length")[0])
        file_name = meta_data.getheaders("Content-Disposition")[0].split('=')[-1]
        name_index =file_name.index(file_nam[:-5])
        file_name = file_name[name_index:]
        if da:
            file_name = da+file_name
        print file_name
        if not os.path.exists(path_folder+'\\'+file_name):
            f = open(path_folder+'\\'+file_name,'wb')
            print "Downloading: %s Bytes: %s" % (path_folder+'\\'+file_name, file_size)
    
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,
        
            f.flush()
            f.close()
        else:
            print file_name+' already exists'
    except Exception,e:
        print 'Couldn\'t download the file from URL : '+ baseurl+'/'+url
    
    
def home():
    hom=br.open(baseurl+'/home.asp')
    html=hom.read()
    soup=bs(html)
    welcome=soup.findAll('table')[1].findAll('td')[0].findAll('font')[0].text.replace('&nbsp;','')
    print '*'*79
    print welcome
    print '*'*79

def timetable():
    
    tt=br.open(baseurl+timtable)
    time.sleep(0.005)
    tt=br.open(baseurl+timtable)
    html=tt.read()
    soup=bs(html)
    subject=[]
    sub_table = soup.findAll('table')[1].findAll('tr') # each row contains a subject
     
    for x in range(0,len(sub_table)):
        sub_attr = soup.findAll('table')[1].findAll('tr')[x].findAll('td')
        for y in range(0,len(sub_attr)):
            value=soup.findAll('table')[1].findAll('tr')[x].findAll('td')[y].text.replace('&nbsp;','')
            if len(value)>0:
                subject.append(value)
        list_subject.append(subject)
        subject=[]
    
    for x in range(0,len(list_subject)):
        try:
            if len(list_subject[x])<10:
                list_subject.remove(sub[x])
        except:pass
    
    for x in range(0,len(list_subject)):                       # Since Lab doesn't have serial no.
        try:                                                   # We remove serial no for all others
            if list_subject[x][5]!='LBC':                      
                list_subject[x]=list_subject[x][1:]                              #
        except:pass                                            #
                                                               
    for x in range(0,5):                                       #
       if len(list_subject[-1])<11:list_subject.remove(list_subject[-1])   # removing the unneccessary values               

def printtime():  
    for x in range(0,len(list_subject)):
        print x,
        try:
            for y in req:
                print '|',
                if y!=9:
                    print list_subject[x][y][0:20].replace('Embedded',''),
                else:
                    print list_subject[x][y][0:15]
            print "*"*79
        except:pass
    print "\b\b"        

def group():
    global list_subject
    e=[]
    temp=[]
    for y in req:
        for x in range(0,len(list_subject)):
            e.append(list_subject[x][y])
        temp.append(e)
        e=[] 
    
    list_subject=temp[:]
                
                            
def Employ():
    
    empid.append('Emp Id')
    for x in range(1,len(list_subject[5])):
        if 'APT' not in list_subject[5][x]:
            l=list_subject[5][x].split('-')
            f=facid %(l[0][:-1].replace(' ','%20'))
            try:
                ff=br.open(f)
                html=ff.read()
                soup=bs(html)
                l=soup.findAll('a')[0].get('href')
                empid.append(l[-5:])
            except:
                 print f
                 empid.append('0')
    list_subject.append(empid)
    
def facchoice(select):
    crsp=crpg%(list_subject[1][select],list_subject[3][select],'')
    url=baseurl+crsp
    k=br.open(url)
    html=k.read()
    soupfac=bs(html)
    for x in range(0,len(soupfac.findAll('table')[1].findAll('tr')[2].findAll('option'))):
        print str(x)+'|'+soupfac.findAll('table')[1].findAll('tr')[2].findAll('option')[x].text
    choice=int(raw_input("select the faculty by entering a the serial number and if you want to choose faculty other than the one you registered add \"d\" at the end \(eg: \"2d\" without the quotes)"))
    ch=soupfac.findAll('table')[1].findAll('tr')[2].findAll('option')[choice].text
    return ch
    

def crs():
    for x in range(0,len(list_subject[0])):
        print str(x)+'|'+list_subject[1][x]+"|"+list_subject[2][x]+"|"+list_subject[3][x]
    select=raw_input("select the subect by entering a the serial number and if you want to choose faculty other than the one you registered add \"d\" at the end (eg: \"2d\" without the quotes)")
    if select[-1]=='d':
        select=int(select[0])
        ch=facchoice(select)
        ch=ch.split(' - ')
        crsp=crpg%(list_subject[1][select],list_subject[3][select],ch[0])
        fac=ch[1]
    else:        
        crsp=crpg%(list_subject[1][int(select)],list_subject[3][int(select)],list_subject[6][int(select)])
        fac=list_subject[5][int(select)]
    url=baseurl+crsp
    k=br.open(url)
    hh = k.read()
    souph = bs(hh)
    input = souph.findAll('input')
    name2 = input[2].get('name')
    name3 = input[3].get('name')
    name4 = input[4].get('name')
    value2 = input[2].get('value')
    value3 = input[3].get('value')
    value4 = input[4].get('value')
    formdat = { name2 : value2,name3 : value3,name4 : value4}
    data_encoded = urllib.urlencode(formdat)
    response = br.open('https://vtop.vit.ac.in/student/coursepage_view3.asp', data_encoded)
    htmla=response.read()
    soupa=bs(htmla)
    lst=[h for h in soupa.findAll('a')]
    link=[each.get('href') for each in lst]
    for x in link :
        try:
            u = urllib2.urlopen(baseurl+"/"+x) #Testing if link is valid and downloadable
        except:
            link.remove(x)
    
    path_folder=createfold(list_subject[1][int(select)]+'-'+list_subject[2][int(select)],fac)
    for x in range(0,len(link)):
        try:
            url = link[x]
            file_nam = lst[x].text
            ##print file_nam
            down(url,file_nam,path_folder)
        except Exception,e:
            print e
            pass            
        print '*'*79
        
if __name__=="__main__":
    global br
    br=login()
    ask()
    home()
    timetable()
    group()
    Employ()
    while True:
        crs()
'''
Created on 2018/03/04

@author: Zizhu Zhang
'''

import requests
import csv
import datetime
import math
from jvn import Jvn 
# from warnings import catch_warnings
url         = "https://jvndb.jvn.jp/search/index.php?mode=_vulnerability_search_IA_VulnSearch&lang=ja&keyword=&useSynonym=1&vendor=&product=&datePublicFromYear=2017&datePublicFromMonth=12&datePublicToYear=2018&datePublicToMonth=12&dateLastPublishedFromYear=2018&dateLastPublishedFromMonth=12&dateLastPublishedToYear=&dateLastPublishedToMonth=&severity%5B0%5D=01&cwe=&searchProductId=&pageNo=2"
origin_url  = "https://jvndb.jvn.jp/search/index.php?mode=_vulnerability_search_IA_VulnSearch&lang=ja&keyword=&useSynonym=1&vendor=&product=&datePublicFromYear=2017&datePublicFromMonth=12&datePublicToYear=2018&datePublicToMonth=12&dateLastPublishedFromYear=2018&dateLastPublishedFromMonth=12&dateLastPublishedToYear=&dateLastPublishedToMonth=&severity%5B%5D=01&cwe=&searchProductId=&skey=a1&pageNo="
filename    = 'result-{date:%Y-%m-%d-%H-%M-%S}.csv'.format( date=datetime.datetime.now() )
# unicodeData.encode('ascii', 'ignore')


#output csv
def export_csv(txt_array,_encoding):
    with open(filename, 'a',encoding=_encoding) as myfile:  
        wr = csv.writer(myfile,lineterminator='\n')    
        wr.writerows([c.strip() for c in r.split(',')] for r in txt_array)
    myfile.close()

#return URL list
def getUrlList(num,origin_url):
    url_list = []
    for i in range(int(num)):
        url_list.append(origin_url + str(i+1))
    return url_list 

def getEachUrlContents(url_list):
    for _index in range(len(url_list)):
        print('               {0}/{1}'.format(_index+1, len(url_list)))
        r       = requests.get(url_list[_index])
        r.encoding=r.apparent_encoding
        demo    =r.content
        
        from bs4 import BeautifulSoup
        soup            = BeautifulSoup(demo,"html.parser")
        tr_list         =soup.select('table.result_class tr')
        #main
        try:
            td_array =[]  
            for tr in tr_list:
                td_str = ''
                tr_list= tr.select('td')
                if len(tr_list) > 0:
                    for td in tr_list:                    
                        if len(td.findChildren())>0  :                        
                            td_str = td_str + td.a['href'] +','
                        else:
                            td_str = td_str + td.text +','
                    if td_str != '':
                        td_array.append(td_str)
                        
                    jvn_url     =tr_list[0].a['href']
                    jvn_title   =tr_list[1].text
                    jvn_cthree  =tr_list[2].text
                    jvn_ctwo    =tr_list[3].text
                    pub_date = tr_list[4].text
                    upd_date = tr_list[5].text
                    now_date=datetime.date.today()
                    jvninfo=Jvn(jvn_url,jvn_title,jvn_cthree,jvn_ctwo,pub_date,upd_date,now_date)
                    
                    jvninfo.action()
            export_csv(td_array, r.encoding)
        except AttributeError:
            print('ERROR!')

def getNumOfFirstPage():
    url =origin_url+'1'
    
    r = requests.get(url)
    _content = r.content
    
    from bs4 import BeautifulSoup
    soup            = BeautifulSoup(_content,"html.parser")    
    all_text        = soup.select(".pager_class .pager_count_class")[0].text
    import re    
    total           = re.findall(r'^\D*(\d+)', all_text)
    totalpagenum    = int(total[0])/100

    return math.ceil(totalpagenum)



def json_auth(gspreadsheet):
    import json
    import gspread
    import oauth2client.client
    
    
    json_key = json.load(open('proJVN-9d35f7ca57ca.json'))
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
             ]
    credentials = oauth2client.client.SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    gc = gspread.authorize(credentials)
      
    wb = gc.open(gspreadsheet)    
#     firstgs = wb.worksheet('01')
    
    
    return gc,wb,credentials
#     
#     val = firstgs.acell('B1').value
#     print(val)

# insert into spreadsheet 
def importgs(filename,gs):
    result = open(filename,'r')
    result_str ='';    
    for line in result:
        result_str+=line;
    
    gs[0].import_csv(gs[1].id,result_str)



    

try:
    num     =getNumOfFirstPage()
    print('************************')
    print('Get JVN Content start')
    urllist = getUrlList(num,origin_url)
    
    getEachUrlContents(urllist)
#     gs = json_auth('test')
#     importgs(filename,gs)

    
    print('Get JVN Content finished')
    print('************************')
except TypeError:
    print('ERROR')



from address import url
import session
from bs4 import BeautifulSoup
from common import *

class Gallog():
    def __init__(self,user_id):
        self.user_id = user_id
        self._gallog_url = url['gallog'] + user_id + "/"
        self._data = {}
    
    def get_total(self):
        return self._total

    #get total count in gallog
    def set_total(self):
        total_res = session.get(self._gallog_url)
        totals = self._get_count_num(total_res.text)

        total_dic = {
            article : totals[0],
            comment : totals[1]
        }
        self._total = total_dic

    #get count in html
    def _get_count_num(self,text):
        count_list = [] #initialize list for return
        bfdoc = BeautifulSoup(text,'html.parser')
        counts = bfdoc.body.find_all('span',{'class':'num'})    #find count value in html
        for cnt in counts:
            cnt = cnt.get_text()[1:-1].replace(',','')  #remove brackets and comma
            count_list.append(int(cnt))
        return count_list

    #get galleries data in html
    def set_gallery_data(self,kind):
        gall_datas = []  #initialize list for return
        list_url = self._gallog_url + kind
        list_res = session.get(list_url)
        bfdoc = BeautifulSoup(list_res.text,'html.parser')
        galleries = bfdoc.body.find_all('ul',{'class':'option_box'})[-1].find_all('li')  #find galleries list in html
        for gallery in galleries:
            code = gallery.get('data-value')
            if code == "":
                continue
            name = gallery.get_text()
            gall_res = session.get(list_url + "?gno=" + code)
            cnt = self._get_count_num(gall_res.text)
            gall_data = {
                'name' : name,
                'code' : code,
                'cnt'  : cnt[0]
            }
            gall_datas.append(gall_data)
        self._data[kind] = gall_datas

    def set_selected_data(self,kind,selected_data):
        total = 0
        for data in selected_data:
            total += data['cnt']
        self._total[kind] = total
        self._data[kind] = selected_data

    def get_gallery_data(self,kind):
        return self._data[kind]

    def get_gallog_url(self):
        return self._gallog_url

    def get_user_id(self):
        return self.user_id
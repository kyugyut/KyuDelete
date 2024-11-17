from address import url
from monkey import magic_code
from bs4 import BeautifulSoup
from common import *
import time
import session
import json

class Delete():
    def __init__(self,user_id):
        self.url = url['gallog'] + user_id + "/"

    def get_page_data(self,kind,gallery):
        self.page_url = self.url + kind + "?gno=" + gallery['code'] 
        page_res = session.get(self.page_url)
        if page_res.text.find('location.replace') != -1:    #if empty gallery
            return []

        bfdoc = BeautifulSoup(page_res.text,'html.parser')

        service_code = bfdoc.find('input',{'name':'service_code'}).get('value')
        scripts = bfdoc.body.find_all('script')
        self._get_service_code(service_code,scripts)

        data_list = bfdoc.find('ul',{'class':'cont_listbox'}).find_all('li')
        return data_list
                        
    def _get_service_code(self,s_code,scripts):
        cryptogram = ""
        for script in scripts:
            s_pos = script.text.find("var _r")
            if s_pos != -1:
                e_pos = script.text.find(";",s_pos)
                cryptogram = script.text[s_pos+13:e_pos-2]
        if cryptogram == "" :
            print(scripts)
            raise Exception("_r value not found")
        self.service_code = magic_code(s_code, cryptogram)

    def delete(self,data):
        del_header = {
            'X-Requested-With': "XMLHttpRequest",
            'Referer': self.page_url
        }
        del_data = {
            'no': data.get('data-no'),
            'ci_t': session.cookie('ci_c'),
            'service_code': self.service_code
        }
        error_count = 0
        while True:
            time.sleep(0.3)
            try:
                del_json = session.post(self.url+url['delete'], del_header, del_data)
                del_text = del_json.text[del_json.text.find('{'):]
                del_json = json.loads(del_text)
            except Exception as e:
                error_count += 1
                get_Exception(e, error_count)
            else:
                if del_json['result'] == "success":
                    return True
                else:
                    return False

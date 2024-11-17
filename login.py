import session
from address import url
from bs4 import BeautifulSoup

#login and return result[bool]
def login(id,pwd):
    auth_header = {'Referer' : url['main']}
    auth_data   = _get_login_data()
    auth_data['user_id'] = id
    auth_data['pw'] = pwd

    session.get(url['sso'])    #set session sso
    auth_res = session.post(url['auth'],auth_header,auth_data).text
    isLogin = auth_res.find('history.back') == -1   #distinct logged in or not
    session.get(url['main']).text   #browse main page again to reduce login miss

    return isLogin

#get login data and return[dictionary]
def _get_login_data():
    login_data = {} #make blank dict for append
    main_res = session.get(url['main']).text   #get main page html text
    main_bfdoc = BeautifulSoup(main_res,'html.parser')  #make text to html doc
    var_list = main_bfdoc.body.find('form',{'id':'login_process'}).find_all('input')    #search login data

    #append data into dict
    for var in var_list:
        name = var.get('name')
        value = var.get('value')
        if(value!=None and value!=''):  #check valid data
            login_data[name] = value

    return login_data
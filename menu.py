from collections import OrderedDict
from getpass import getpass
from gallog import Gallog
from login import login
from delete import Delete
from common import *

#return choice(int,not index)
def _select_menu(selection_list,select_message):
    for pos,selection in enumerate(selection_list):
        print("{0}. {1}".format(pos+1,selection))
    print()
    while True:
        choice = input(select_message)
        length = len(selection_list)
        if _is_valid_choice(choice,length):
            choice = int(choice)
            break

    return choice

#check whether input is integer and in range
def _is_valid_choice(choice,count):
    try:
        choice = int(choice)    #check valid integer
    except Exception:
        print("숫자만 입력하실 수 있습니다")
        return False
    else:    
        if choice > count or choice <= 0: #check out of range
            print("잘못된 번호를 입력하셨습니다")
            return False
        else:
            return True

#return user_id
def _login():
    clear()
    print("아이디와 비밀번호를 입력해주세요")

    #loop until login success
    while True:
        user_id = input("아이디　: ")
        user_pw = getpass("비밀번호: ")
        clear()
        print("로그인중... ",end='')
        login_result = login(user_id,user_pw)
        if login_result:
            print("로그인 성공!")
            break
        print("로그인 실패! 다시 입력해주세요")
    global gallog
    gallog = Gallog(user_id)

def show():
    #load gallog info
    if gallog is None:
        _login()
    print("갤로그를 불러오는 중...")
    gallog.set_total()
    print("게시글을 불러오는 중...")
    gallog.set_gallery_data(article)
    print("댓글을 불러오는 중...")
    gallog.set_gallery_data(comment)

    clear()
    total = gallog.get_total()
    article_data = gallog.get_gallery_data(article)
    comment_data = gallog.get_gallery_data(comment)
    print("{0}개의 게시글과 {1}개의 댓글이 검색되었습니다\n".format(total[article],total[comment]))

    if total[article]==0 and total[comment]==0:     #check zero activity
        print("지울 수 있는 글이나 댓글이 없습니다!")
        pause()
        quit()

    main_list = ["게시글과 댓글 삭제","게시글 삭제","댓글 삭제","종료"]
    main_msg  = "원하시는 작업을 선택해주세요 : "
    choice = _select_menu(main_list,main_msg)
        
    #show sub menu and delete
    if choice == 1:
        if _isZero(article):
            return
        if _isZero(comment):
            return
        _select_gallery(article)
        _select_gallery(comment)
        _delete_process(article)
        _delete_process(comment)
        print("게시글과 댓글 삭제가 완료되었습니다")
        pause()
        clear()
    elif choice == 2:
        if _isZero(article):
            return
        _select_gallery(article)
        _delete_process(article)
        print("게시글 삭제가 완료되었습니다")
        pause()
        clear()
    elif choice == 3:
        if _isZero(comment):
            return
        _select_gallery(comment)
        _delete_process(comment)
        print("댓글 삭제가 완료되었습니다")
        pause()
        clear()
    else:
        quit()
    
def _isZero(kind):
    clear()
    total = gallog.get_total()[kind]
    if total == 0:
        print("지울 수 있는 {0}이 없습니다!".format(kor[kind]))
        pause()
        clear()
        return True
    return False


#return false when zero activity
def _select_gallery(kind):
    gallery_list = gallog.get_gallery_data(kind)
    total = gallog.get_total()[kind]

    print("{0} 선택".format(kor[kind]))
    print("{0}개의 {1}이 검색되었습니다\n".format(total,kor[kind]))
    sub_list = ["갤러리 전체 삭제","선택한 갤러리 삭제"]
    sub_msg  = "원하시는 작업을 선택해주세요 : "
    choice = _select_menu(sub_list,sub_msg)

    if choice == 2:     #show submenu when parts of galleries
        clear()
        gallery_cnt = len(gallery_list)

        print("{0} 선택".format(kor[kind]))
        print("{0}개의 갤러리가 검색되었습니다".format(gallery_cnt))
        print("쉼표로 구분하여 여러 갤러리를 선택하실 수 있습니다\n")
        for pos,gallery in enumerate(gallery_list):
            print("{0}. {1} 갤러리".format(pos+1,gallery['name']))
        print()

        #loop until choosing galleries ends
        is_select_success = False
        while not is_select_success:
            choices = input("{0}을 삭제할 갤러리를 선택해 주세요 : ".format(kor[kind]))
            
            selected_gallery_list = []     #initialize for return
            choices = choices.split(',')
            is_select_success = True
            for choice in choices[:]:
                if _is_valid_choice(choice,gallery_cnt):
                    selected_gallery_list.append(gallery_list[int(choice)-1])
                else:
                    is_select_success = False     #loop when invalid input is mixed
                    break

            if is_select_success:            #when selection success        
                selected_gallery_list = list({selected_gallery['name']: selected_gallery for selected_gallery in selected_gallery_list}.values())   #remove duplication
                for pos,selected_gallery in enumerate(selected_gallery_list):
                    name = selected_gallery['name']
                    if pos + 1 == len(selected_gallery_list):
                        query = "\n{0} 갤러리에 있는 모든 {1}을 삭제하시겠습니까? [y/n] "
                        yesorno = input(query.format(name,kor[kind])).lower()
                    else:
                        print("{0}, ".format(name),end='')
                if yesorno != 'y' and yesorno != 'yes':  #loop false when decision true
                    is_select_success = False
        gallog.set_selected_data(kind,selected_gallery_list)
    clear()

def _delete_process(kind):
    user_id = gallog.get_user_id()
    delete = Delete(user_id)
    print("*** {0} 삭제 시작 ***".format(kor[kind]))
    gallery_list = gallog.get_gallery_data(kind)
    for gallery in gallery_list:
        current = 0
        while current < gallery['cnt']:
            data_list = delete.get_page_data(kind,gallery)
            if len(data_list) == 0:     #when gallery is empty, break loop
                break
            for data in data_list:
                isDelete = delete.delete(data)
                if isDelete:
                    current += 1
                    print("{0} 갤러리 삭제 중 ... [{1}/{2}]".format(gallery['name'],current,gallery['cnt']),end='\r')
        print("{0} 갤러리 삭제 완료                        ".format(gallery['name']))
    print("*** {0} 삭제가 완료되었습니다 ***\n".format(kor[kind]))

gallog = None
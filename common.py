import os
import platform

def pause():
    if platform.system() == "Linux":
        command = "read -n1 -r -p \"Press any key to continue...\""
    elif platform.system() == "Darwin":
        command = ""    #명령어 뭐지;
    elif platform.system() == "Windows":
        command = "pause"
    os.system(command)

def clear():
    if platform.system() == "Linux":
        command = "clear"
    elif platform.system() == "Darwin":
        command = ""    #명령어 뭐지;
    elif platform.system() == "Windows":
        command = "cls"
    os.system(command)

def get_Exception(e,try_var):
    if try_var >= 7:
        print("오류가 발생했습니다!")
        print(type(e))
        print(e)
        pause()
        quit()

article = 'posting'
comment = 'comment'
kor = {
    article : "게시글",
    comment : "댓글"
}
article_k = "게시글"
comment_k = "댓글"
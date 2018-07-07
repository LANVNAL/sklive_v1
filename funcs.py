# -*- coding: utf-8 -*-
import requests
import json

def logincheck(username,password):
    login_url = 'http://jwgl.sdust.edu.cn/app.do?method=authUser&xh={}&pwd={}'.format(username, password)
    rqs = requests.post(login_url)
    flag = json.loads(rqs.text)
    flagg = flag['flag']
    #print flagg
    if flagg == '1':
        return 'ok'
    else:
        return 'error'

def login(username,password):
    global S
    login_url = 'http://jwgl.sdust.edu.cn/app.do?method=authUser&xh={}&pwd={}'.format(username,password)
    S = requests.Session()
    login = S.post(login_url)
    j = json.loads(login.text)
    token = j['token']
    return token

def userinfo(username,password):
    global S
    token = login(username, password)
    headers = {"token": token}
    data = {"userAccountType": "2"}
    info_url = "http://jwgl.sdust.edu.cn:80/app.do?method=getUserInfo&xh={}".format(username)
    userinfo = S.post(info_url, headers=headers, data=data)
    return json.loads(userinfo.text)

def curriculum(username,password,semester,week):
    global S
    token = login(username, password)
    headers = {"token": token}
    data = {"userAccountType": "2"}
    curriculum_url = "http://jwgl.sdust.edu.cn/app.do?method=getKbcxAzc&xh={}&xnxqid={}&zc={}".format(username,semester,week)
    curriculum = S.post(curriculum_url, headers=headers, data=data)
    return json.loads(curriculum.text)


def grade(username,password,semester):
    global S
    token = login(username, password)
    headers = {"token": token}
    data = {"userAccountType": "2"}
    grade_url = 'http://jwgl.sdust.edu.cn/app.do?method=getCjcx&xh={}&xnxqid={}'.format(username,semester)
    grade = S.post(grade_url, headers=headers, data=data)
    return json.loads(grade.text)

def exam_arrangement(username,password):
    global S
    token = login(username, password)
    headers = {"token": token}
    data = {"userAccountType": "2"}
    exam_url = 'http://jwgl.sdust.edu.cn/app.do?method=getKscx&xh={}'.format(username)
    exam_arrangement = S.post(exam_url, headers=headers, data=data)
    #print exam_arrangement.text
    return json.loads(exam_arrangement.text)

def express(company,number):
    url = "https://www.kuaidi100.com/query?type={}&postid={}".format(company, number)
    res = requests.get(url)
    infojson = json.loads(res.text)
    info = json.dumps(infojson, ensure_ascii=False)
    return infojson






if __name__ == '__main__':
    username = '201601060210'
    password = 'skctf2018'
    semester = '2017-2018-2'
    week = '12'
    token = login(username,password)
    headers = {"token":token}
    data = {"userAccountType": "2"}
    userinfo(username,headers,data)
    curriculum(username,semester,week)
    grade(username,semester)
    exam_arrangement(username)
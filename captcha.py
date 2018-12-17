#-*- coding: utf-8 -*-
import os
import re
import random


def get_captcha():
    path = os.path.join(os.path.dirname(__file__), 'captcha', 'jpgs/')
    file_list = get_file(path)
    uuid = re.findall("ques(.*?).jpg", file_list[random.randint(0, len(file_list)-1)])[0]
    answer = get_answer(uuid)
    return [uuid, answer[4]]


def get_answer(uuid):
    path = os.path.join(os.path.dirname(__file__), 'captcha', 'ans/')
    filename = path+'ans'+uuid+'.txt'
    f = open(filename, 'r')
    answer = f.read()
    answer = re.findall('= (.*?)\\n', answer)
    return answer


def get_file(path):
    for root, dir, filename in os.walk(path):
        file_list = filename
    return file_list


def check_captcha(x, y, uuid):
    answer = get_answer(uuid)
    if(float(answer[0]) <= float(x) <= float(answer[0])+float(answer[2])):
        if(float(answer[1]) <= float(y) <= float(answer[1])+float(answer[3])):
            return True
    return False

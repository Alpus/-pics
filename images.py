# -*- coding: utf-8 -*-

try:
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    pass

import json
import pickle
import os.path
import random

short_names = ["Левитан", "Айвазовский", "Рубенс", "Серов", "Шишкин", "Кандинский", "Брюллов", "Аргунов", "Васнецов",
        "Верещагин", "Пукирев", "Суриков", "Репин", "Рублев", "Крамской", "Водкин", "Врубель", "Йорданс", "Иорданс", "Ван Гог",
        "Гойен", "Гоген", "Джордано", "Матисс", "Грёз", "Сезанн", "Якобс", "Ренуар", "Моне", "Мане", "Пикассо", "Рембрандт",
        "Вос", "Рафаэль", "Кранах", "Делакруа", "Иорданс", "Кранах", "Тинторетто", "Тициан", "Рибера", "Карраччи",
        "Ван Дейк", "Браувер"]

def load_images():
    json_file = open("static/images_db", "r")
    images = json.load(json_file)
    return images
    
images = load_images()

def get_image_link(image):
    return image['data']['general']['mainImage']['preview']

def get_image_name(image):
    return image['data']['general']['name']

def get_image_author(image):
    return image['data']['general']['author']

def get_authors():
    authors = set()
    for x in map(get_image_author, images):
        if x:
            authors.add(x)
    return authors

def get_pic():
    image = random.choice(images)
    return {'author': get_image_author(image),
            'title': get_image_name(image),
            'link': get_image_link(image)}

def get_rand_name_except_author(author):
    short_name = "Pushin Alexander"
    for name in short_names:
        if name in author:
            short_name = name
            break
    image = random.choice(images)
    while short_name.lower() in get_image_author(image).lower():
        image = random.choice(images)
    return get_image_author(image)

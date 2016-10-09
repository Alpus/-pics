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

def find_short_name(author):
    for name in short_names:
        if name.lower() in author.lower():
            return name
    
def find_long_name(short_name):
    return random.choice(filter(lambda x: short_name.lower() in x.lower(), get_authors()))

def get_rand_names_except_author(author):
    short_name = find_short_name(author)
    name_1 = random.choice(short_names)
    while name_1 == short_name:
        name_1 = random.choice(short_names)
    name_2 = random.choice(short_names)
    while name_2 == short_name or name_2 == name_1:
        name_2 = random.choice(short_names)
    return find_long_name(name_1), find_long_name(name_2)

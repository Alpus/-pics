# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import jinja2
import uuid

from images import get_rand_name_except_author, get_pic
from random import shuffle

import json
import pickle


questions = dict()

top_file = "static/top.dat"
def read_top():
    try:
        return pickle.load(open(top_file, 'rb'))
    except:
        pickle.dump([('Енот уже не тот', 0)], open(top_file, 'wb'))
        return pickle.load(open(top_file, 'rb'))


def change_top(needed_login, needed_score):
    top = read_top()
    flag = False

    for n in range(len(top)):
        login, score = top[n]
        if needed_login == login:
            flag = True
            if score < needed_score:
                top[n] = login, needed_score
            else:
                break

    if not flag:
        top.append((needed_login, needed_score))

    top = sorted(top, key=lambda x: -x[1])
    pickle.dump(top, open(top_file, 'wb'))


def make_new_question(old_count):
    question_id = str(uuid.uuid4())
    image = get_pic()
    print(image)
    authors = [
        (image['author'], question_id),
        (get_rand_name_except_author(image['author']), question_id),
        (get_rand_name_except_author(image['author']), question_id)
    ]
    shuffle(authors)
    for num, (author, question_id) in enumerate(authors):
        authors[num] = (num, author, question_id)

    questions[question_id] = {'name': image['author'], 'count': old_count}
    return question_id, image, authors


class CheckAnswer(tornado.web.RequestHandler):
    def post(self):
        if not self.get_cookie("login"):
            self.render("pages/login.html")
        else:
            name, question_id = self.get_argument("value").split(';')
            print('real', questions[question_id]['name'])
            print('get', name)

            if questions[question_id]['name'] == name:
                questions[question_id]['count'] += 1
                question_id, image, pic_list = make_new_question(questions[question_id]['count'])
                self.write(json.dumps({
                        "verdict": "OK", "link": image['link'],"pic_name": image['title'],
                        "authors": pic_list,
                        'count': questions[question_id]['count']
                    })
                )
            else:
                change_top(self.get_cookie("login"), int(questions[question_id]['count']))
                self.write(json.dumps({"verdict": "ERR", 'count': questions[question_id]['count']}))
                del questions[question_id]


class MainPage(tornado.web.RequestHandler):
    def get(self):
        login = self.get_argument('login', None)
        if not self.get_cookie("login"):
            if not login:
                self.render("pages/login.html")
            else:
                self.set_cookie('login', login)
                self.redirect('/')
        else:
            question_id, image, authors = make_new_question(0)
            self.render(
                'pages/main.html',
                link=image['link'],
                pic_name=image['title'],
                authors=authors,
                top=read_top()
            )


routes = [
    (r'/', MainPage),
    (r'/answer', CheckAnswer),
]


app = tornado.web.Application(routes)
app.listen(80)
tornado.ioloop.IOLoop.current().start()

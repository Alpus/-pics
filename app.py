import tornado.ioloop
import tornado.web
import jinja2
import uuid

import images
from random import shuffle

import json

questions = dict()

def make_new_pic_list():
	question_id = str(uuid.uuid4())
	image = images.get_pic()
	authors = [(image['author'], question_id)]
	map(authors.append, [(get_rand_name_except(image['author']), question_id), (get_rand_name_except(image['author']), question_id)])

	for num, (author, question_id) in enumerate(shuffle(authors)):
		authors[num] = (num, author, question_id)

	return question_id, image, authors

class CheckAnswer(tornado.web.RequestHandler):
    def post(self):
        name, question_id = self.get_argument("value").split(';')
        if questions[question_id]['name'] == name:
        	questions[question_id]['count'] += 1
        	question_id, image, pic_list = make_new_pic_list()
        	self.write(json.dumps(
        		{"verdict": "OK", "link": image['link'], "pic_name": image['title'], "value": ';'.join(image['author'], question_id), "authors": pic_list})
        	)
        else:
        	self.write(json.dumps({"verdict": "ERR", 'count': questions[question_id]['count']}))
        	del questions[question_id]


class MainPage(tornado.web.RequestHandler):
    def get(self):
        self.render('pages/main.html', pic_name='У ванькова мелкий писюничк', authors=[(0, 'Репин', 123), (1, 'Хуепин', 123), (2, 'Пидор', 123)])



routes = [
	(r'/', MainPage),
	(r'/answer', CheckAnswer)
]


app = tornado.web.Application(routes)
app.listen(8000)
tornado.ioloop.IOLoop.current().start()

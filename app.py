from flask import Flask, render_template
import mongoengine
import datetime


class Author(mongoengine.Document):
    username = mongoengine.StringField(max_length=255, required=True)
    password = mongoengine.StringField(max_length=255, required=True)
    email = mongoengine.StringField(max_length=255, required=True)


class Post(mongoengine.Document):
    created_at = mongoengine.DateTimeField(default=datetime.datetime.now, required=True)
    modified_at = mongoengine.DateTimeField(default=datetime.datetime.now, required=True)
    title = mongoengine.StringField(max_length=255, required=True)
    author = mongoengine.ReferenceField(Author)
    slug = mongoengine.StringField(max_length=255, required=True)
    body = mongoengine.StringField(required=True)


class Config(mongoengine.Document):
    title = mongoengine.StringField(max_length=255, required=True)


app = Flask(__name__)
app.config.update({"DEBUG" : True})
mongoengine.connect('polonium')


@app.route('/')
def show_homepage():
    return render_template('base.html', title=Config.objects[0].title)


if __name__ == '__main__':
    app.run()
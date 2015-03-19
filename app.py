from flask import Flask, render_template, session, request, redirect, url_for, flash
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
    name = mongoengine.StringField(max_length=255, required=True)


DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
mongoengine.connect('polonium')


@app.route('/')
def index():
    return render_template('index.html', config=Config.objects[0] )


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            if request.form['password'] != Author.objects.get(username=request.form['username']).password:
                error = '密码错误'
            else:
                session['logged_in'] = True
                session['username'] = request.form['username']
                return redirect(url_for('index'))
        except mongoengine.DoesNotExist:
            error = '该用户不存在'
    return render_template('login.html', error=error, config=Config.objects[0])


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('您已注销')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

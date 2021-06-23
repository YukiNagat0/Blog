from os import path
from typing import Union
from datetime import datetime

from flask import Flask, request, redirect, render_template
from flask_wtf import CSRFProtect

from werkzeug.utils import secure_filename

from data import db_session

from data.posts import Posts

from forms.edit_post_form import EditPostForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET_KEY'
csrf_protect = CSRFProtect(app)

UPLOAD_FOLDER = 'static/posts_img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATA_BASE = 'db/blog.sqlite'
app.config['DATA_BASE'] = DATA_BASE


def edit_post_in_data_base(form: EditPostForm, post: Union[Posts, None]):
    db_sess = db_session.create_session()

    post_title = form.title.data
    post_text = form.text.data
    post_author = form.author.data

    post_image = form.image.data
    # --- Фотография ---
    if not post_image:
        post_image_name = ''  # Картинки нет
    else:
        current_id = db_sess.query(Posts).order_by(Posts.id.desc()).first()
        current_id = current_id.id + 1 if current_id else 1

        real_image_name = secure_filename(post_image.filename)
        post_image_name = f'{current_id}{real_image_name[real_image_name.rfind("."):]}'
        post_image.save(path.join(app.config['UPLOAD_FOLDER'], post_image_name))
    # --- Фотография ---

    if not post:  # Добавление поста
        post = Posts()

        post.title = post_title
        post.image_name = post_image_name
        post.text = post_text
        post.author = post_author
        post.date = datetime.now()

        db_sess.add(post)
    else:  # редактирование
        post.title = post_title
        post.image_name = post_image_name
        post.text = post_text
        post.author = post_author
        post.date = datetime.now()

        db_sess.merge(post)
    db_sess.commit()
    db_sess.close()

    return redirect('/')


@app.route('/')
def index():
    params = {'title': 'Blog', 'UPLOAD_FOLDER': app.config['UPLOAD_FOLDER']}

    db_sess = db_session.create_session()

    posts = db_sess.query(Posts).order_by(Posts.id.desc()).all()
    view = render_template('blog.html', **params, posts=posts)

    db_sess.close()

    return view


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    params = {'title': 'Добавление поста', 'action_type': 'Добавление поста', 'submit_text': 'Добавить'}

    form = EditPostForm()
    params['form'] = form

    if form.validate_on_submit():
        return edit_post_in_data_base(form, None)

    return render_template('edit_post.html', **params)


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id: int):
    params = {'title': 'Редактирование поста', 'action_type': 'Редактирование поста', 'submit_text': 'Редактировать'}

    form = EditPostForm()
    params['form'] = form

    db_sess = db_session.create_session()
    post: Posts = db_sess.query(Posts).filter(Posts.id == post_id).first()
    db_sess.close()

    if not post:
        return redirect('/')

    if request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text
        form.author.data = post.author
    elif form.validate_on_submit():
        return edit_post_in_data_base(form, post)

    return render_template('edit_post.html', **params)


@app.route('/delete_post/<int:post_id>')
def delete_post(post_id: int):
    db_sess = db_session.create_session()

    post = db_sess.query(Posts).filter(Posts.id == post_id).first()
    if post:
        db_sess.delete(post)
        db_sess.commit()

    db_sess.close()

    return redirect('/')


def main():
    db_session.global_init(app.config['DATA_BASE'])
    app.run('127.0.0.1', 8080)


if __name__ == '__main__':
    main()

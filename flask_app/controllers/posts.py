from flask_app import app  
from flask_app.models import post
from flask import render_template, request, session, flash, redirect

# @app.route('/<topic_name>')
# def show_topic(topic_name):
#     data = {
#         'topic': topic_name
#     }
#     return render_template('topic.html', posts=post.Post.get_by_topic(data))

@app.route('/new_post')
def new_post():
    return render_template('create_post.html')

@app.route('/process_post', methods=['POST'])
def process_post():
    data = {
        'title': request.form['title'],
        'post': request.form['post'],
        'topic': request.form['topic'],
        'users_id': session['id']
    }
    post_id = post.Post.add_post(data)
    data2 = {
        'id': int(post_id)
    }
    this_post = post.Post.get_post_by_id(data2)
    return redirect(f'/{this_post.topic}/post/{this_post.id}')

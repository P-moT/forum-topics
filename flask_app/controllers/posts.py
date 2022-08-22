from turtle import pos
from xml.etree.ElementTree import Comment
from flask_app import app  
from flask_app.models import post, user
from flask_app.models.user import User
from flask import render_template, request, session, flash, redirect


@app.route("/dashboard")
def dashboard():
    user_data = {
        'id': session['id']
    }
    user = User.get_user_by_id(user_data)
    posts = post.Post.get_all_posts()
    return render_template("dashboard.html", user=user, posts=posts)


# @app.route('/<topic_name>')
# def show_topic(topic_name):
#     data = {
#         'topic': topic_name
#     }
#     return render_template('topic.html', posts=post.Post.get_by_topic(data), topic_name = topic_name)

# updated version
@app.route('/sports')
def show_sports():
    user_data = {
        'id': session['id']
    }
    session_user = User.get_user_by_id(user_data)
    posts = post.Post.get_all_posts_desc()
    return render_template("sports.html", posts=posts, session_user=session_user)

# updated version
@app.route('/science')
def show_science():
    user_data = {
        'id': session['id']
    }
    session_user = User.get_user_by_id(user_data)
    posts = post.Post.get_all_posts_desc()
    return render_template("science.html", posts=posts, session_user=session_user)

# updated version
@app.route('/technology')
def show_technolocy():
    user_data = {
        'id': session['id']
    }
    session_user = User.get_user_by_id(user_data)
    posts = post.Post.get_all_posts_desc()
    return render_template("technology.html", posts=posts, session_user=session_user)

# @app.route('/new_post')
# def new_post():
#     return render_template('create_post.html')

# updated version
@app.route('/new_post')
def new_post():
    user_data = {
        "id": session["id"]
    }
    user = User.get_user_by_id(user_data)
    return render_template('create_post.html', user=user)



# @app.route('/process_post', methods=['POST'])
# def process_post():
#     data = {
#         'title': request.form['title'],
#         'post': request.form['post'],
#         'topic': request.form['topic'],
#         'users_id': session['id']
#     }
#     post_id = post.Post.add_post(data)
#     data2 = {
#         'id': int(post_id)
#     }
#     this_post = post.Post.get_post_by_id(data2)
#     return redirect(f'/{this_post.topic}/post/{this_post.id}')

# updated version
@app.route('/process_post', methods=['POST'])
def process_post():
    # form validation
    if not post.Post.validate_post_form(request.form):
        return redirect("/new_post")
    post.Post.add_post(request.form)
    return redirect("/dashboard")

@app.route('/delete_post/<topic_name>/<int:id>')
def delete_post(topic_name, id):
    post_data = {
        'id': id
    }
    post.Post.delete_post(post_data)
    return redirect(f'/{topic_name}')

@app.route('/<topic>/post/<int:id>')
def show_post(id, topic):
    user_data = {
        'id': session['id']
    }
    session_user = User.get_user_by_id(user_data)
    post_data = {
        'id': id,
        'topic':topic
    }
    this_post = post.Post.get_one_post(post_data)
    return render_template("post.html", this_post=this_post, session_user=session_user, comments=post.Comment.get_comments(post_data))


@app.route('/add_comment/<topic_name>/<int:post_id>', methods=['POST'])
def add_comment(topic_name, post_id):
    if not post.Comment.validate_comment(request.form['comment']):
        return redirect(f'/{topic_name}/post/{post_id}')
    data = {
        'posts_id': post_id,
        'users_id': session['id'],
        'comment': request.form['comment']
    }
    post.Comment.create_comment(data)
    return redirect(f'/{topic_name}/post/{post_id}')

@app.route('/delete_comment/<topic_name>/<int:post_id>/<int:id>')
def delete_comment(topic_name, post_id, id):
    comment_data = {
        'id': id
    }
    post.Comment.delete_comment(comment_data)
    return redirect(f'/{topic_name}/post/{post_id}')

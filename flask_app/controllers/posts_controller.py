from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.models.user_model import User
from flask_app.models.post_model import Post

@app.route('/new_post', methods= ['POST'])
def create_post():
    if 'user_id' not in session:
        redirect ('/logout')
    if not Post.validate_posts(request.form):
        return redirect ('/')
    data = {
        "content": request.form['content'],
        "user_id": session['user_id']
    }
    print(data)
    Post.save(data)
    return redirect ('/wall')

@app.route('/delete_post/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect ('/logout')
    Post.delete(id)
    return redirect ('/wall')





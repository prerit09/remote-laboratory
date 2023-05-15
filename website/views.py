from .common_code import result
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Exercise
# Post, Comment, Like
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    # posts = Post.query.all()
    return render_template("home.html", user=current_user, 
                        #    posts=posts
                           )

@views.route("/exercises", methods=['GET', 'POST'])
@login_required
def exercises():
    exercises = Exercise.query.all()
    return render_template('exercises.html', user=current_user, exercises=exercises)

@views.route("/exercise/<exercise_id>", methods=['GET', 'POST'])
@login_required
def exercise(exercise_id):
    exercise = Exercise.query.filter_by(id=exercise_id).first()
    if request.method == 'POST':
        code = request.form.get('code')
        stdin = request.form.get('stdin')
        expected = exercise.solution
        output = result(code, stdin, expected)
        print(result)

        return render_template("code.html", user=current_user, exercise=exercise)

    print("in progress")
    return render_template("code.html", user=current_user, exercise=exercise)

# @views.route("/submission/<submission_id>", methods=['POST'])
# @login_required
# def submission(submission_id):
#     if request.method == 'POST':
#         print(submission_id)

#     # exercise = Exercise.query.filter_by(id=exercise_id).first()
#     return render_template("views.home", user=current_user, exercise=exercise)

@views.route("/create-exercise", methods=['GET', 'POST'])
@login_required
def create_exercise():
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        solution = request.form.get('solution')
        if not title:
            flash('Title cannot be empty', category='error')
        elif not description:
            flash('Description cannot be empty', category='error')
        elif not solution:
            flash('Solution cannot be empty', category='error')
        else:
            exercise = Exercise(title=title, description=description, solution=solution, author=current_user.id)
            db.session.add(exercise)
            db.session.commit()
            flash('Exercise created!', category='success')
            return redirect(url_for("views.home"))
    return render_template('exercises.html', user=current_user)

# @views.route("/create-post", methods=['GET', 'POST'])
# @login_required
# def create_post():
#     if request.method == "POST":
#         text = request.form.get('text')
#         if not text:
#             flash('Post cannot be empty', category='error')
#         else:
#             post = Post(text=text, author=current_user.id)
#             db.session.add(post)
#             db.session.commit()
#             flash('Post created!', category='success')
#             return redirect(url_for("views.home"))
#     return render_template('create_post.html', user=current_user)

# @views.route("/delete-post/<id>")
# @login_required
# def delete_post(id):
#     post = Post.query.filter_by(id=id).first()    
#     if not post:
#         flash("Post does not exist", category="error")
#     elif current_user.id != post.author:
#         flash("You do not have permission to delete this post.", category='error')
#     else:
#         db.session.delete(post)
#         db.session.commit()
#         flash('Post deleted.', category='success')


#     return redirect(url_for("views.home"))

# @views.route("/posts/<username>")
# @login_required
# def posts(username):
#     user = User.query.filter_by(username=username).first()
#     if not user:
#         flash('No user with that username exists', category='error')
#         return redirect(url_for('views.home'))
    
#     posts = user.posts
    

#     return render_template("posts.html", user=current_user, posts=posts, username=username)

# @views.route("/create-comment/<post_id>", methods=['POST'])
# @login_required
# def create_comment(post_id):
#     text = request.form.get('text')
#     if not text:
#         flash('Comment cannot be empty', category='error')
#     else:
#         post = Post.query.filter_by(id=post_id)
#         if post:
#             comment = Comment(text=text, author=current_user.id, post_id=post_id)
#             db.session.add(comment)
#             db.session.commit()
#             flash('Post deleted.', category='success')
#         else:
#             flash('Post does not exist', category='error')

#     return redirect(url_for('views.home'))
    
# @views.route("/delete-comment/<comment_id>")
# @login_required
# def delete_comment(comment_id):
#     comment = Comment.query.filter_by(id=comment_id).first()
#     if not comment:
#         flash('Comment does not exist.', category='error')
#     elif current_user.id != comment.author and current_user.id != comment.post.author:
#         flash('You do not have permission to delete this comment.', category='error')
#     else:
#         db.session.delete(comment)
#         db.session.commit()
#         flash('Comment deleted.', category='success')
    
#     return redirect(url_for('views.home'))

# @views.route("/like-post/<post_id>", methods=['POST'])
# @login_required
# def like(post_id):
#     post = Post.query.filter_by(id=post_id).first()
#     like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

#     if not post:
#         return jsonify({"error" : "Post does not exist."}, 400)
#     elif like:
#         db.session.delete(like)
#         db.session.commit()
#     else:
#         like=Like(author=current_user.id, post_id=post_id)
#         db.session.add(like)
#         db.session.commit()

#     return jsonify({"likes": len(post.likes), "liked" : current_user.id in map(lambda x: x.author, post.likes)})
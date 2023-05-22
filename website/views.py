from .common_code import result
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Exercise, TestCase, Submission
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
    testcases = TestCase.query.filter_by(exercise_id=exercise.id).all()
    submissions = Submission.query.filter_by(exercise_id=exercise.id).all()
    if request.method == 'POST':
        code = request.form.get('code')
        stdin = request.form.get('stdin')
        if(request.form['action'] == "Run"):
            print("Code Running")
            print(code)
            output = result(code, stdin)
            print(output)
            return render_template("code.html", user=current_user, exercise=exercise, output=output)
        elif(request.form['action'] == "Test" or request.form['action'] == "submit"):
            print("Code under Test")
            score=0
            if exercise.solution is not None:
                print("Single Solution")
            
                expected = exercise.solution
                output = result(code, stdin, expected)
                if(output['status']['description'] == 'Accepted'):
                    score+=1
                print(output)
                return render_template("code.html", user=current_user, exercise=exercise, output=output)
            elif exercise.testcase :
                print("Multiple Test Cases")

                outputs=[]
                for testcase in testcases:
                    output = result(code, testcase.input, testcase.output)
                    outputs.append(output)

                passed=0
                for output in outputs:  
                    print(output['status']['description'])
                    if(output['status']['description'] == 'Accepted'):
                        passed+=1
                
                if passed == len(testcases):
                    html = "Congratulations! All test cases passed!"
                else:
                    html = str(passed) + "/" + str(len(testcases))

                if(request.form['action'] == "submit"):
                    score = passed
                    submission = Submission(code=code, score=score, author=current_user.id, exercise_id=exercise.id)
                    db.session.add(submission)
                    db.session.commit()

                return render_template("code.html", user=current_user, exercise=exercise, output=None, testcase=html)
        # else:
        #     print("code submitted")
        #     code = request.form.get('code')


            return render_template("code.html", user=current_user, exercise=exercise, output=None)

    print("in progress")
    return render_template("code.html", user=current_user, exercise=exercise, output=None)

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

        if not solution:
            count=1
            test_cases_dict = {}
            stdin = request.form.get("stdin"+str(count))
            while(stdin is not None):
                stdin = request.form.get("stdin"+str(count))
                test_cases_dict[stdin] = request.form.get("stdout"+str(count))
                count+=1
                stdin = request.form.get("stdin"+str(count))

            exercise = Exercise(title=title, description=description, author=current_user.id)
            db.session.add(exercise)
            db.session.commit()
            
            for stdin in test_cases_dict.keys():
                testcase = TestCase(input=stdin, output=test_cases_dict[stdin], author=current_user.id, exercise_id=exercise.id)
                db.session.add(testcase)
                db.session.commit()

            print(exercise.testcase)
            flash('Exercise created!', category='success')

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
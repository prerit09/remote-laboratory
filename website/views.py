from io import BytesIO
from .common_code import result
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from .models import User, Exercise, TestCase, Submission
# Post, Comment, Like
from . import db

def save_submission(code, exercise, passed):
    score = passed
    try:
        submission = Submission(code=code, score=score, author=current_user.id, exercise_id=exercise.id)
        db.session.add(submission)
        db.session.commit()
        flash('Submission Saved For Exercise!', category='success')
        print("Submission Saved")
    except Exception as e:
        if("UNIQUE constraint failed: submission.exercise_id" in str(e)):
            flash('Submission Already Done!', category='error')
        db.session.rollback()
        print("Here : " + str(e) + "End")

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    # posts = Post.query.all()
    return render_template("home.html", user=current_user, 
                        #    posts=posts
                           )
@views.route("/delete-exercise/<exercise_id>", methods=['GET', 'POST'])
@login_required
def delete_exercise(exercise_id):
    exercise = Exercise.query.filter_by(id=exercise_id).first()
    # print(exercise.id)
    if not exercise:
        flash('Exercise does not exist.', category='error')
    elif current_user.id != exercise.author:
        flash('You do not have permission to delete this exercise.', category='error')
    else:
        db.session.delete(exercise)
        db.session.commit()
        flash('Exercise deleted.', category='success')
    
    return redirect(url_for('views.exercises'))

@views.route("/view-submissions/<exercise_id>", methods=['GET', 'POST'])
@login_required
def view_submissions(exercise_id):
    submissions = Submission.query.filter_by(exercise_id=exercise_id).all()
    print(submissions)
    for submission in submissions:
        print(submission.code)
        print(submission.score)
        print(submission.user.username)
    return render_template('submissions.html', user=current_user, submissions=submissions)

@views.route("/playground", methods=['GET', 'POST'])
@login_required
def playground():
    if request.method == 'POST':
        code = request.form.get('code')
        stdin = request.form.get('stdin')
        if(request.form['action'] == "Run"):
            print("Code Running")
            print(code)
            output = result(code, stdin)
            print(output)
            return render_template("code.html", user=current_user, exercise=None, output=output)
    
    return render_template('code.html', user=current_user, exercise=None, output=None)

@views.route("/exercises", methods=['GET', 'POST'])
@login_required
def exercises():
    exercises = Exercise.query.all()

    ## TBD
    submission = Submission.query.filter_by(author=current_user.id, exercise_id=1)
    print(submission)    
    return render_template('exercises.html', user=current_user, exercises=exercises)

@views.route("/exercise/description/<exercise_id>", methods=['GET', 'POST'])
@login_required
def download_exercise_description(exercise_id):
    download = Exercise.query.filter_by(id=exercise_id).first()
    print(download.description_file_name)
    return send_file(BytesIO(download.description_file_data), download_name=download.description_file_name)

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
            return render_template("code.html", user=current_user, exercise=exercise, output=output, code=code, stdin=stdin)
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
                if(request.form['action'] == "submit"):
                    save_submission(code,exercise,score)
                    return redirect(url_for("views.home"))
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
                save_submission(code,exercise,passed)
                return redirect(url_for("views.home"))

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
        countdown = request.form.get('countdown')
        description_file = request.files['descriptionfile']

        if not solution:
            count=1
            test_cases_dict = {}
            stdin = request.form.get("stdin"+str(count))
            while(stdin is not None):
                stdin = request.form.get("stdin"+str(count))
                test_cases_dict[stdin] = request.form.get("stdout"+str(count))
                count+=1
                stdin = request.form.get("stdin"+str(count))

            if not description_file:
                if not countdown:
                    exercise = Exercise(title=title, description=description, author=current_user.id)
                else:
                    exercise = Exercise(title=title, description=description, author=current_user.id, countdown=countdown)
            else:
                if not countdown:
                    exercise = Exercise(title=title, description=description, description_file_name=description_file.filename, description_file_data=description_file.read(), author=current_user.id)
                else:
                    exercise = Exercise(title=title, description=description, description_file_name=description_file.filename, description_file_data=description_file.read(), author=current_user.id, countdown=countdown)
            db.session.add(exercise)
            db.session.commit()
            
            for stdin in test_cases_dict.keys():
                testcase = TestCase(input=stdin, output=test_cases_dict[stdin], author=current_user.id, exercise_id=exercise.id)
                db.session.add(testcase)
                db.session.commit()

            print(exercise.testcase)
            flash('Exercise created!', category='success')

        else:
            if not description_file:
                if not countdown:
                    exercise = Exercise(title=title, description=description, solution=solution, author=current_user.id)
                else:
                    exercise = Exercise(title=title, description=description, solution=solution, author=current_user.id, countdown=countdown)
            else:
                if not countdown:
                    exercise = Exercise(title=title, description=description, description_file_name=description_file.filename, description_file_data=description_file.read(), solution=solution, author=current_user.id)
                else:
                    exercise = Exercise(title=title, description=description, description_file_name=description_file.filename, description_file_data=description_file.read(), solution=solution, author=current_user.id, countdown=countdown)
            db.session.add(exercise)
            db.session.commit()
            flash('Exercise created!', category='success')
            return redirect(url_for("views.home"))
    return render_template('create_exercise.html', user=current_user)

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
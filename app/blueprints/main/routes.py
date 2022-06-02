from statistics import StatisticsError
from flask import render_template, current_app as app, request, redirect, url_for, flash
from datetime import datetime as dt
from app.blueprints.users.models import Post, User
from app import db
from flask_login import current_user, login_required
from datetime import datetime


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
   
    if request.method == 'POST':
        # grab form data
        comment = request.form.get('post')
        mood = request.form.get('moodSelection')
        sleep = request.form.get('sleepSelection')
        ate = bool(request.form.get('meal'))
        hygiene = bool(request.form.get('hygiene'))
        meds = bool(request.form.get('meds'))
        active = bool(request.form.get('active'))


        # create new post
        p = Post(body=comment, mood=mood, sleep=sleep, ate=ate, hygiene=hygiene, meds=meds, active=active, author=current_user.get_id())
        
        # stage post to be committed to the database
        db.session.add(p)

        # send that/those change(s) to the database
        db.session.commit()

        flash('You have created a new mood', 'info')
        return redirect(url_for('home'))
    
    
    return  render_template('main/home.html', posts=[post.to_dict() for post in Post.query.filter_by(author=current_user.get_id()).order_by(Post.date_created.desc()).all()])
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        form_data = request.form

        # update the user's information
        user = User.query.get(current_user.get_id())
         # if the user wants to change their password
         # check if the (confirm) password fields are the same
        user.first_name = form_data.get('first_name')
        user.last_name = form_data.get('last_name')
        user.email = form_data.get('email')

        if len(form_data.get('password')) == 0:
            pass
        elif form_data.get('password') == form_data.get('confirm_password'):
            user.generate_password(form_data.get('password'))
        else:
            flash('There was an error updating your password', 'danger')
            return redirect(url_for('profile'))

        db.session.commit()
        # print(form_data.get('first_name'))
         # print(form_data.get('last_name'))
        # print(form_data.get('email'))
        # print(form_data.get('password'))
        # print(form_data.get('confirm_password'))
        flash('You have updated your information', 'primary')
        return redirect(url_for('profile'))
    return render_template('main/profile.html',  sleepCounter=[post.sleep for post in Post.query.filter_by(author=current_user.get_id())], moodCounter=[post.mood for post in Post.query.filter_by(author=current_user.get_id())], ateCounter=[post.ate for post in Post.query.filter_by(author=current_user.get_id())], activeCounter=[post.active for post in Post.query.filter_by(author=current_user.get_id())],
  medCounter=[post.meds for post in Post.query.filter_by(author=current_user.get_id())], hygieneCounter=[post.hygiene for post in Post.query.filter_by(author=current_user.get_id())])

@app.route('/post/delete/<post_id>')
def post_delete(post_id):

    post_to_delete = Post.query.filter_by(id=post_id).first()
        # stage post to be committed to the database
        
    db.session.delete(post_to_delete)

        # send that/those change(s) to the database
    db.session.commit()

    flash('You have deleted the mood', 'info')
    return redirect(url_for('home'))


@app.route('/contact')
def contact():
    return '<h1>Contact</h1>'
from flask import Flask,request,render_template,redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db,db,User,Feedback
from forms import UserForm,UserFormLogin,FeedBackForm
from sqlalchemy.exc import IntegrityError
#from map import key,requests
app = Flask(__name__)

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_hw_db'
app.config['SECRET_KEY'] = 'asdasd'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_home():
    return redirect('/register')

@app.route('/register',methods=['POST','GET'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        try:
            new_user = User.register(username,password,email,first_name,last_name)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
        except IntegrityError:
            #flash('already have that username','danger')
            form.username.errors.append('Username taken. Please pick another')
            return render_template('register.html',form=form)
        flash('Welcome!','success')
        return redirect(f'/users/{new_user.id}')
    
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = UserFormLogin()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username,password)
        if user:
            flash(f'Welcome back, {user.username}','info')
            session['username'] = user.username
            return redirect(f'/users/{user.id}')
        else:
            form.username.errors = ['invalid username/password']
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    flash('Logged out','info')
    return redirect('/')

@app.route('/users/<int:id>')
def show_user_page(id):
    if 'username' not in session:
        flash('Please login or signup','danger')
        return redirect('/')
    user = User.query.get(id)
    return render_template('user.html',user=user)

@app.route('/users/<int:id>/delete',methods=['POST'])
def delete_user(id):
    if session['username'] == User.query.get(id).username:

        u =User.query.get(id)
        db.session.delete(u)
        Feedback.query.filter_by(username=u.username).delete()
        db.session.commit()
        return redirect('/login')
    
@app.route('/users/<int:id>/feedback/add',methods=['POST','GET'])
def add_feedback(id):
    form = FeedBackForm()
    if session['username']:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            username = session['username']
            n = Feedback.new_feedback(title,content,username)
            db.session.add(n)
            db.session.commit()
            return redirect(f'/users/{id}')
    return render_template('feedback_form.html',form=form)

@app.route('/feedback/<int:id>/edit',methods=['POST','GET'])
def edit_feedback(id):
    form = FeedBackForm()
    if session['username']:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feed = Feedback.query.get(id)
            feed.title = title
            feed.content = content
            db.session.commit()
            return redirect(f'/users/{feed.user.id}')
    return render_template('feedback_form.html',form=form)

@app.route('/feedback/<int:id>/delete',methods=['POST'])
def delete_feed(id):
    feed = Feedback.query.get(id)
    if session['username'] == feed.user.username:
        db.session.delete(feed)
        db.session.commit()
        return redirect(f'/users/{feed.user.id}')

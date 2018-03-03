from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, RadioField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import os

app = Flask(__name__)


######################################################################################
######################################## Config ######################################
######################################################################################

#config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass.'
app.config['MYSQL_DB'] = 'database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL
mysql = MySQL(app)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

def loggin_check(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized request. Please sign in.', 'danger')
            return redirect(url_for('login'))
    return wrap

#user sign in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        cur = mysql.connection.cursor()

        #get user
        result = cur.execute('SELECT * FROM users WHERE username = %s', [username])
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            user_id = data['user_id']

            if sha256_crypt.verify(password_input, password):
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = user_id
                flash('Welcome! You have successfully signed in.', 'success')
                return redirect(url_for('main'))
            else:
                error = 'Invalid Login Credentials'
                app.logger.info('Password Not Matched')
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
            mysql.connection.commit()
            cur.close()
            flash("You're account has been created.", 'success')
            return redirect(url_for('main'))
        except Exception as e:
            if '1062' in str(e):
                flash("Username already taken", 'danger')
                return redirect(url_for('register'))

    return render_template('register.html', form=form)


######################################################################################
######################################## Routes ######################################
######################################################################################

@app.route("/")
def main():
    
    #Get top ten syllabi from syllabus_views table
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT syl_id, COUNT(*) AS freq FROM syllabus_views GROUP BY syl_id ORDER BY freq DESC")
    pop_syl = cur.fetchall()
    cur.close()

    #loop through popular syllabi and query from syllabus_info table
    popular_syllabi_by_views = []

    if result > 0:
        cur = mysql.connection.cursor()
        for i in pop_syl:
            result = cur.execute("SELECT * FROM syllabus_info WHERE syl_id = %s", [i['syl_id']])
            si = cur.fetchone()
            popular_syllabi_by_views.append(si)
        cur.close()
        return render_template('index.html', active='index', syllabi = popular_syllabi_by_views)
    else:
        msg = 'No Articles Found'
        return render_template('index.html', msg=msg)
    #close connection
    cur.close()

class SyllabusSearchForm(Form):
    search = StringField('Search', [validators.Length(min=1, max=100)])
    browseradio = RadioField('Search By: ', choices=[('all','All'),
    ('title','Title'),('subject','Subject'),('description','Description')], 
    default='all')
	
@app.route("/browse", methods=['GET','POST'])
def browse():
    form = SyllabusSearchForm(request.form)
    if request.method == 'POST':
        search = request.form['search']
        browseradio = request.form['browseradio']
        print(browseradio)

        if browseradio == 'title':
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM syllabus_info WHERE title LIKE %s", (['%' + search + '%']))
            syllabi = cur.fetchall()
            cur.close()
            return render_template('browse.html', active='browse', form = form, syllabi = syllabi)
        elif browseradio == 'subject':
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM syllabus_info WHERE subject LIKE %s", (['%' + search + '%']))
            syllabi = cur.fetchall()
            cur.close()
            return render_template('browse.html', active='browse', form = form, syllabi = syllabi)
        elif browseradio == 'description':
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM syllabus_info WHERE description LIKE %s", (['%' + search + '%']))
            syllabi = cur.fetchall()
            cur.close()
            return render_template('browse.html', active='browse', form = form, syllabi = syllabi)
        else:
            cur = mysql.connection.cursor()
            result = cur.execute("SELECT * FROM syllabus_info WHERE (title LIKE %s) OR (subject LIKE %s) OR (description LIKE %s)", (['%' + search + '%', '%' + search + '%', '%' + search + '%']))
            syllabi = cur.fetchall()
            cur.close()
            return render_template('browse.html', active='browse', form = form, syllabi = syllabi)
    
    return render_template('browse.html', active='browse', form = form, syllabi = "")
	
@app.route("/about")
def about():
    return render_template('about.html', active='about')

@app.route('/syllabus/<string:id>/')
def article(id):

    syllabus_saved_already = False

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM syllabus_saves WHERE user_id = %s", [session['user_id']])
    syl_save = cur.fetchall()
    
    for i in syl_save:
        if id == str(i['syl_id']):
            syllabus_saved_already = True
    cur.close()
    
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM syllabus_info WHERE syl_id = %s", [id])
    syl = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO syllabus_views(syl_id) VALUES(%s)", (id))
    mysql.connection.commit()
    cur.close()

    return render_template('syllabus.html', syl=syl, syllabus_saved_already = syllabus_saved_already)

@app.route("/dashboard")
@loggin_check
def dashboard():

    userID = str(session['user_id'])

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM syllabus_info WHERE user_id = %s", [userID])
    made_syllabi = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM syllabus_saves WHERE user_id = %s", [userID])
    syl_saves = cur.fetchall()
    cur.close()

    user_saved_syllabi = []

    cur = mysql.connection.cursor()
    for i in syl_saves:
        result = cur.execute("SELECT * FROM syllabus_info WHERE syl_id = %s", [i['syl_id']])
        si = cur.fetchone()
        user_saved_syllabi.append(si)
    cur.close()
        
    return render_template('dashboard.html', active='dashboard', saved_syllabi = user_saved_syllabi, made_syllabi = made_syllabi)

@app.route('/logout')
@loggin_check
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('main'))


######################################################################################
######################################## API #########################################
######################################################################################

################################ Create Functions ####################################

class SyllabusForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    subject = StringField('Subject', [validators.Length(min=1, max=200)])
    description = StringField('Description', [validators.Length(min=1, max=500)])
    body = TextAreaField('Body')

@app.route('/add_syllabus', methods=['GET', 'POST'])
@loggin_check
def add_syllabus():
    form = SyllabusForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        subject = form.subject.data
        description = form.description.data
        body = form.body.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO syllabus_info(title, subject, description, body, user_id) VALUES(%s, %s, %s, %s, %s)",(title, subject, description, body, session['user_id']))
        mysql.connection.commit()
        cur.close()

        flash('Syllabus Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add.html', form=form)

@app.route('/add_syllabus_save/<string:id>', methods=['POST'])
@loggin_check
def add_syllabus_save(id):

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO syllabus_saves(syl_id, user_id) VALUES(%s, %s)",(id, session['user_id']))
        mysql.connection.commit()
        cur.close()

        flash('Syllabus Saved', 'success')

        return redirect(url_for('dashboard'))

################################ Update Functions ####################################

@app.route('/edit_syllabus/<string:id>', methods=['GET', 'POST'])
@loggin_check
def edit_syllabus(id):
    
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM syllabus_info WHERE syl_id = %s", [id])

    syllabus = cur.fetchone()
    cur.close()
    # Get form
    form = SyllabusForm(request.form)

    # Populate article form fields
    form.title.data = syllabus['title']
    form.subject.data = syllabus['subject']
    form.description.data = syllabus['description']
    form.body.data = syllabus['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        subject = request.form['subject']
        description = request.form['description']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        cur.execute ("UPDATE syllabus_info SET title=%s, subject=%s, description=%s, body=%s WHERE syl_id=%s",(title, subject, description, body, id))
        mysql.connection.commit()
        cur.close()

        flash('Syllabus Updated', 'success')

        return redirect(url_for('dashboard'))
    if syllabus['user_id'] == session['user_id']:
        return render_template('edit.html', form=form)
    else:
        flash('You do not have permission to edit the requested syllabus', 'danger')
        return redirect(url_for('main'))

################################ Delete Functions ####################################

@app.route('/delete_syllabus/<string:id>', methods=['POST'])
@loggin_check
def delete_syllabus(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM syllabus_info WHERE syl_id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash('Syllabus Deleted', 'success')

    return redirect(url_for('dashboard'))

@app.route('/remove_saved_syllabus/<string:id>', methods=['POST'])
@loggin_check
def remove_saved_syllabus(id):
    # Create cursor
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM syllabus_saves WHERE syl_id = %s AND user_id = %s", [id, session['user_id']])
    mysql.connection.commit()
    cur.close()

    flash('Syllabus Unsaved', 'success')

    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    app.secret_key= os.urandom(24)
app.run(debug=True)

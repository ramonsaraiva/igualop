import os

from sqlite3 import dbapi2 as sqlite3

from flask import Flask
from flask import render_template
from flask import request
from flask import g

from werkzeug import secure_filename

# config

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({
    'DATABASE': os.path.join(app.root_path, 'mon.sqlite'),
    'SECRET_KEY': 'development key',
    'USERNAME': 'admin',
    'PASSWORD': 'default',
    'UPLOAD_PATH': os.path.join(app.root_path, 'upload'),
    'ALLOWED_EXT': set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', 'tar', 'gz'])
})

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def home():
    return render_template('home.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXT']

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    uploaded = False
    db = get_db()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        f = request.files['file']
        if f and title and allowed_file(f.filename):
            filename = secure_filename(f.filename)

            # add a suffix to avoid overriding files
            suffix = 1
            while os.path.isfile(os.path.join(app.config['UPLOAD_PATH'], filename)):
                    filename = '{0}{1}.{2}'.format(filename.split('.')[0], str(suffix), filename.split('.')[1])
                    suffix += 1

            f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            query = ('insert into upload (title, description, filename) VALUES (\'{0}\', \'{1}\', \'{2}\')'.format(title, description, filename))
            print(query)
            db.execute(query)
            db.commit()
            uploaded = True

    query = db.execute('select title, filename from upload order by id desc')
    entries = query.fetchall()
    return render_template('upload.html', entries=entries, uploaded=uploaded, ext=app.config['ALLOWED_EXT'])

@app.route('/dev')
def dev():
    return render_template('dev.html')

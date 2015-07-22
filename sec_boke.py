import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


# create our little application :)
app = Flask(__name__)


APP_PATH = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'test.db'


def get_db():
    db = sqlite3.connect(os.path.join(APP_PATH, DB_NAME))

    return db





def execute_sql(sql, args=()):#sqlite3's operators
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, args)
    result = cur.fetchall()
    db.commit()
    cur.close()
    return result


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor()
        cur.execute("create table if not exists user( username char(20), password char(50))")
        cur.close()
        if execute_sql("select username from user where username = ?", (request.form['username'],))== []:
            error = 'Invalid username'
            return render_template('login.html', error=error)
        elif execute_sql("select password from user where password= ?", (request.form['password'],))== []:
            error = 'Invalid password'
            return render_template('login.html', error=error)
        else:
            return redirect(url_for('blog_list'))
    else:
        return render_template('login.html')


@app.route('/blog')
def blog_list():
    db = get_db()
    cur = db.cursor()
    cur.execute("create table if not exists blog(id integer primary key autoincrement,title text not null,content text not null)")
    cur.close()
    blogs = execute_sql("SELECT * FROM blog ORDER BY id DESC")
    return render_template('blog_list.html', blogs=blogs)


@app.route('/blog/<blog_id>')
def blog(blog_id):
    blogs = execute_sql("SELECT * FROM blog WHERE id=?", (blog_id))
    if len(blogs) == 0:
        return redirect(url_for('blog_list'))
    return render_template('view_blog.html', blog=blogs[0])


@app.route('/blog/add', methods=['GET', 'POST'])
def add_blog():

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        execute_sql("INSERT INTO blog VALUES (NULL ,? ,?)", (title, content))


        return redirect(url_for('blog_list'))
    else:
        return render_template('new_blog.html')


if __name__ == '__main__':
    app.run(debug=True)







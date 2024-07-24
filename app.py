from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import TodoForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # セッションのための秘密鍵

db = SQLAlchemy(app)

# Todoモデルの定義
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# データベースの初期化をアプリコンテキストで行う関数
def init_db():
    with app.app_context():
        db.create_all()

# アプリコンテキストでデータベースを初期化する
init_db()

# ルートURLの設定
@app.route('/', methods=['GET', 'POST'])
def index():
    form = TodoForm(request.form)

    if request.method == 'POST' and form.validate():
        new_todo = Todo(title=form.title.data)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))

    todos = Todo.query.all()
    return render_template('index.html', todos=todos, form=form)

# Todoの完了/未完了の切り替え
@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    todo = Todo.query.get(todo_id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))

# Todoの削除
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

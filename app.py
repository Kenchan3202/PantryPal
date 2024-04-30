from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return 'login failed'
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('password wrong')
            return redirect(url_for('register'))
        # 添加更多的用户验证和存储逻辑

        flash('register succed')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main/Items', methods=['GET', 'POST'])
def Items():
    items = [
        {"name": "Milk", "expiry_date": "2024-05-01"},
        {"name": "Bread", "expiry_date": "2024-05-03"},
        {"name": "Apple", "expiry_date": "2024-04-28"}
    ]
    return render_template('main/Items.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
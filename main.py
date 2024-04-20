from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Secret key for session management

# Hardcoded admin credentials (you should use a more secure method in production)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"


# Store the data entered in the admin page in files
data1_file = "data1.txt"
data2_file = "data2.txt"


# Function to check if user is logged in
def is_logged_in():
    return 'username' in session


# Function to write data to file
def write_to_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)


# Function to read data from file
def read_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['username'] = username
            return redirect(url_for('admin_panel'))
        else:
            return render_template('admin_login.html', error="Invalid username or password")
    return render_template('admin_login.html')


@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    if not is_logged_in():
        return redirect(url_for('admin'))

    if request.method == 'POST':
        data1 = request.form.get('data1','Connecting...')
        data2 = request.form.get('data2','Connecting...')
        write_to_file(data1_file, data1)
        write_to_file(data2_file, data2)
    return render_template('admin_panel.html')


@app.route('/get_data1')
def get_data1():
    return read_from_file(data1_file)


@app.route('/get_data2')
def get_data2():
    return read_from_file(data2_file)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

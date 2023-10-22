# import Flask, render_template
from flask import Flask, render_template

# create flask object
app = Flask(__name__)

# create default route which renders index.j2
@app.route('/')
def index():
    return render_template('index.j2')

# create route for login which renders login.j2
@app.route('/login')
def login():
    return render_template('login.j2')

# create route for animals which renders animals.j2
@app.route('/animals')
def animals():
    return render_template('animals.j2')

# create listener running in debug mode on port 3000
if __name__ == '__main__':
    app.run(debug=True, port=3000)

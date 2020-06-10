from flask import *


app = Flask(__name__)

@app.route('/LoginForm')
def loginFormPage():
    return render_template('LoginForm.html')



if __name__ == "__main__":
    app.run(debug = True)
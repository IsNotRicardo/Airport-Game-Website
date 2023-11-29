from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/path.unknown')
def base_app():
    return redirect(url_for('home_app'))


@app.route('/path.unknown/home')
def home_app():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/path.unknown')
def base_route():
    return redirect(url_for('home_route'))


@app.route('/path.unknown/home')
def home_route():
    return render_template('home.html')


@app.route('/path.unknown/tutorial')
def tutorial_route():
    return render_template('tutorial.html')


@app.route('/path.unknown/game')
def game_route():
    return render_template('game.html')


@app.route('/path.unknown/leaderboard')
def leaderboard_route():
    return render_template('leaderboard.html')


@app.route('/path.unknown/info')
def info_route():
    return render_template('info.html')


if __name__ == '__main__':
    app.run(debug=True)

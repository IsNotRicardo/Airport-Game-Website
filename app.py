from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/path.unknown')
def base_app():
    return redirect(url_for('game_app'))


@app.route('/path.unknown/game')
def game_app():
    return render_template('game.html')


if __name__ == '__main__':
    app.run(debug=True)

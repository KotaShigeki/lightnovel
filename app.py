# インストールした「flask」モジュールをインポートする
from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from culculation import judgement
from flask_caching import Cache

# インスタンス化する
app = Flask(__name__) #アンダースコア(_)をnameの左右にそれぞれ2つずつ書く

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# the toolbar is only enabled in debug mode:
#app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
#app.config['SECRET_KEY'] = '<replace with a secret key>'

#toolbar = DebugToolbarExtension(app)

#ルーティング設定をする
@app.route('/')
@cache.cached(timeout=60)
def index():
    return render_template('index.html')

@app.route("/calc",methods=['GET','POST'])
def calculation():
    if request.method == "GET":
        return render_template('calculation.html')
    elif request.method == "POST":
        txt = request.form ['txt']
        try:
            answer = judgement(txt)
        except Exception as e:
            answer = f"エラーが発生しました: {str(e)}"

        return render_template('calculation.html', result=answer)
        

if __name__ == "__main__": #最後に記述する
    app.run(debug=False)
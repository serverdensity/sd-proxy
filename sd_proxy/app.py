from flask import Flask
from gevent.monkey import patch_all

app = Flask(__name__)
patch_all()


@app.route('/postback/')
def postbacks():
    return ''

if __name__ == '__main__':
    app.run()

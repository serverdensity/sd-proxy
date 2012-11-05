from flask import Flask
from gevent.monkey import patch_all

app = Flask(__name__)
patch_all()


@app.route('/postback/', methods=('POST',))
def postbacks():
    return 'OK'

if __name__ == '__main__':
    app.run()

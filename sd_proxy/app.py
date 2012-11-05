from flask import Flask
from gevent.monkey import patch_all

from . import settings

app = Flask(__name__)
patch_all()


@app.route('/postback/', methods=('POST',))
def postbacks():
    return u'OK'

if __name__ == '__main__':
    app.run()

from flask import Flask, jsonify, request, make_response
import thea.core.kernel as k
import sys

g = k.Graph()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(t1='Hello World!', t2="This is cool!")


@app.route('/kbus', methods=["POST"])
def commandBus():
    try:
        resp = dict(state=0, err=False)
        body = request.get_json()
        print(body)
        code  = body['cmd']
        exec(code)
    except Exception as ex:
        resp = {"err": True, "msg": str(ex)}
    return jsonify(resp)


# Only for direct run
if __name__ == '__main__':
    app.run(port=3737)


def run():
    context = ('thea/core/ssl_cert/server.crt', 'thea/core/ssl_cert/server.key')
    app.run(port=3737, ssl_context=context, threaded=True, debug=False)

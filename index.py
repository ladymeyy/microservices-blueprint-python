from flask import Flask, request, jsonify
import pprint
from calendar import timegm
from datetime import datetime
import _strptime

from producer import init

def convert_to_time_ms(timestamp):
    return 1000 * timegm(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').timetuple())

app = Flask(__name__)
app.config["DEBUG"] = True
p = init()


@app.route('/')
def health_check():
  return 'This service is healthy.'

@app.route('/get-my-blessing', methods=['GET'])
def fortune():
    return jsonify({
        'data': 'Mey the force be with you.',
        'status': 'awesome'
    }), 200


@app.route('/public/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.get_json()
    pprint.pprint(content)
    metrics = p.metrics()
    pprint.pprint(metrics)

    p.send('my-first-topic', content)
    return jsonify({"uuid": uuid})



#TODO add incoming requests counter & send to metrics.

@app.route('/search', methods=['POST'])
def search():
  return jsonify(['series', 'series2'])



@app.route('/query', methods=['POST'])
def query():
    req = request.get_json()
    data = [
        {
            "target": req['targets'][0]['target'],
            "datapoints": [
                [861, convert_to_time_ms(req['range']['from'])],
                [767, convert_to_time_ms(req['range']['to'])]
            ]
        }
    ]
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


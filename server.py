from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'DEEPCONVCHESS'

@app.route('/image/process', methods=['POST'])
def process_image():
    image_data = request.json.get('image')
    print(image_data)

    return jsonify({'message': 'Image sent successfully.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
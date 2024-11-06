from flask import Flask, request, jsonify
from PIL import Image
import io

app = Flask(__name__)


@app.route('/')
def index():
    instructions = {
        "message": "Welcome to  the Flask Route API Application!",
        "usage": {
            "convert": {
                "method": "POST",
                "description": "Convert an image from one format to another.",
                "endpoint": "/convert",
                "parameters": {
                    "image": "The image file to convert.",
                    "output_format": "The desired output format. Available formats: JPEG, PNG, BMP, GIF."
                }
            },
            "": {
                "method": "GET or POST",
                "description": "Description of your assigned package functionality.",
                "endpoint": "/your_route",
                "parameters": {
                    "input": "User input required by your assigned package."
                }
            }
        }
    }
    return jsonify(instructions)


@app.route('/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files or 'output_format' not in request.form:
        return jsonify({'error': 'Image file and output format are required.'}), 400

    image_file = request.files['image']
    output_format = request.form['output_format'].upper()

    if output_format not in ['JPEG', 'jpg', 'PNG', 'BMP', 'GIF']:
        return jsonify({'error': 'Unsupported output format.'}), 400

    try:
        image = Image.open(image_file.stream)
        img_io = io.BytesIO()
        image.save(img_io, output_format)
        img_io.seek(0)
        return send_file(img_io, mimetype=f'image/{output_format.lower()}')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/pyaztro', methods=['GET'])
def pyaztro():
    pass


if __name__ == '__main__':
    app.run()

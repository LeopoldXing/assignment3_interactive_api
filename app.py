from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
import nltk

app = Flask(__name__)

# Download necessary NLTK data files for tokenization and POS tagging
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


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
            "tokenize": {
                "method": "POST",
                "description": "Get token and tag of a provided sentence.",
                "endpoint": "/tokenize",
                "parameters": {
                    "sentence": "Sentence provided by the user."
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

    if output_format not in ['JPEG', 'PNG', 'BMP', 'GIF']:
        return jsonify({'error': 'Unsupported output format.'}), 400

    try:
        image = Image.open(image_file.stream)
        img_io = io.BytesIO()
        image.save(img_io, output_format)
        img_io.seek(0)
        return send_file(img_io, mimetype=f'image/{output_format.lower()}')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tokenize', methods=['POST'])
def tokenize():
    sentence = request.form.get('sentence', '')

    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400

    # Tokenize and tag the sentence
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    res = {
        "sentence": sentence,
        "tokens": tokens,
        "tagged": tagged
    }
    return jsonify(res)


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from PIL.ExifTags import TAGS
import os

from meta_gen import MetaReader

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_exif_data(image_path):
    reader = MetaReader(image_path)
    exif_data = reader.execute()
    # image = Image.open(image_path)
    # exif_data = {}
    # try:
    #     info = image._getexif()
    #     if info:
    #         for tag, value in info.items():
    #             tagname = TAGS.get(tag, tag)
    #             exif_data[tagname] = value
    # except AttributeError:
    #     exif_data = None
    return exif_data

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser also
        # submits an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            exif_data = get_exif_data(filepath)
            return render_template('index.html', filepath=filepath, exif_data=exif_data)

    return render_template('index.html', filepath=None, exif_data=None)

if __name__ == "__main__":
    app.run(debug=True)

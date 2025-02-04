from flask import Flask, request, redirect, url_for
from PIL import Image
import sqlite3
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY, name TEXT, data BLOB, size INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/')
def upload_form():
    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit">
    </form>
    '''

@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # Measure the size of the image
        img = Image.open(file)
        img_size = os.path.getsize(file.filename)
        file.seek(0)  # Reset the file pointer after reading

        if img_size <= app.config['MAX_CONTENT_LENGTH']:
            # Save image data to the database
            file_data = file.read()
            encoded_file = base64.b64encode(file_data).decode('utf-8')

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO images (name, data, size) VALUES (?, ?, ?)", (file.filename, encoded_file, img_size))
            conn.commit()
            conn.close()

            return redirect(url_for('upload_form'))
        else:
            return 'File is too large!'

    return 'No file uploaded!'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

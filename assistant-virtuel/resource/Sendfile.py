from flask import Flask,send_from_directory

app = Flask(__name__)
# Specify directory to download from . . . 
DOWNLOAD_DIRECTORY = "<your folder directory>"

@app.route('/get-files/<path:path>',methods = ['GET','POST'])
def get_files(path):

    """Download a file."""
    try:
        return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8000, threaded = True, debug = True)
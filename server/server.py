"""
Flask server for PLCH
"""

from flask import Flask
app = Flask(__name__)

#https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

@app.route("/")
def hello():
    return "hello world"
    # return flask.render_template("danny_html")

@app.route("/api/0.1/textbooks", methods=['GET'])
def get_textbooks():
    # get textbooks from mongodb
    #return jsonify(textbookthing)

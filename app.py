from flask import Flask

app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)
    app.run(port=7000)

@app.route("/")
def hello_world():
    
    return "<h1>Hello, World!</h1>"
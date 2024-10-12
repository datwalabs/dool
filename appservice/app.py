from flask import Flask

app = Flask(__name__)

# Basic route for the homepage
@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    # Run the app on localhost (127.0.0.1) with debug mode on
    app.run(debug=True)

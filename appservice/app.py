from flask import Flask

# services
import Services.UserService as UserService

app = Flask(__name__)

# Basic route for the homepage
@app.route('/')
def home():
    return UserService.hello()

# User Management
@app.route('/users', methods=['POST'])
def create_user():
    UserService.create_user(None)
    return '', 201

@app.route('/users')
def get_users():
    return UserService.hello()


if __name__ == '__main__':
    # Run the app on localhost (127.0.0.1) with debug mode on
    app.run(debug=True)

## Overview

I started with a legacy Flask-based user management API that worked but was messy. I didn’t add any new features just focused on cleaning it up, improving structure, fixing security issues, and making it more maintainable.

### Setup (Should take < 5 minutes)
```bash
# Clone/download this repository
# Navigate to the Parent directory

# Install dependencies
pip install -r requirements.txt

# Start the application
python main.py

# The API will be available at http://localhost:5000


### Testing the Application
The application provides these endpoints:
- `GET /` - Health check
- `GET /users` - Get all users
- `GET /user/<id>` - Get specific user
- `POST /users` - Create new user
- `PUT /user/<id>` - Update user
- `DELETE /user/<id>` - Delete user
- `GET /search?name=<name>` - Search users by name
- `POST /login` - User login


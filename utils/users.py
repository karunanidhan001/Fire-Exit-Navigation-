# Dummy data for user authentication
users_db = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3',
}

def check_user(username, password):
    """Check if the provided username and password are correct."""
    if users_db.get(username) == password:
        return True
    return False

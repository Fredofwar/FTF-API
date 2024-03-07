from src.models.User import User

class AuthService():
    
    @classmethod
    def login(cls, user):
        authenticated_user = None
        authenticated_user = User(user.id, user.username, user.password, user.email)
        return authenticated_user;           
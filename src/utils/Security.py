from decouple import config
import datetime
import jwt
import pytz

class Security():
    secret = config('JWT_KEY')
    tz = pytz.timezone("America/Mexico_City")
    
    @classmethod
    def generate_token(self, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=self.tz),
            'exp': datetime.datetime.now(tz=self.tz) + datetime.timedelta(hours=1),
            'username': authenticated_user.username,
            'password': authenticated_user.password,
            'roles': ['Administrator', 'User']
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")
    
    @classmethod
    def has_access(self, encoded_token):
        if (encoded_token != None and len(encoded_token) > 0):
            payload =  self.get_payload_token(encoded_token)
            if 'iat' in payload and 'exp' in payload and 'username' in payload and 'password' in payload:
                return True
        return False
    
    @classmethod
    def verify_token(self, headers):
        encoded_token = self.get_token_from_request(headers)
        if(encoded_token != None and len(encoded_token) > 0 ):
            try:
                payload = self.get_payload_token(encoded_token)
                roles = list(payload['roles'])
                if 'Administrator' in roles:
                    return True
                return False
            except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                return False  
        return False
    
    @classmethod
    def get_payload_token(self, encoded_token):
        return jwt.decode(encoded_token, self.secret, algorithms=["HS256"])
    
    @classmethod
    def get_token_from_request(self, headers):        
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]
            return encoded_token
        else:
            return None
""" Registration / Login Helper """

def register(client):
    return client.post('auth/register', data={
        'username':'testuser',
        'email':'test@sample.com',
        'password':'somepassword'})    

def login(client):
    return client.post('auth/login', data={
        'username':'testuser',
        'email':'test@sample.com',
        'password':'somepassword'})
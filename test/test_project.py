import io 
import time
from website.models import User

def test_home(client):
    response = client.get("/")
    assert b"<title>Redirecting...</title>" in response.data

def test_student(client, app):
    response = client.post("/sign-up", data={"email":"test@test.com", "username":"username", "password1":"password1", "password2":"password1"})
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "test@test.com"
        assert User.query.first().username == "username"

def test_playground(client):
    
    client.post("/sign-up", data={"email":"test@test.com", "username":"username", "password1":"password1", "password2":"password1"})
    client.post("/login", data={"email":"test@test.com","password":"password"})
    response = client.post("/playground", data={"code":"""
                                                        #include<iostream> 
                                                        \nusing namespace std;
                                                        int main() 
                                                        { 
                                                            cout<<\"Hello World\"; 
                                                            return 0; 
                                                        }
                                                """, "action" : "Run"
                                                })
    assert b"Hello World" in response.data

def test_admin(client):
    client.post("/sign-up", data={"email":"admin@gmail.com", "username":"admin", "password1":"admin", "password2":"admin"})
    client.post("/login", data={"email":"admin@gmail.com","password":"admin"})
    response = client.get("/admin")
    assert b"Admin Portal" in response.data
    
# def test_not_admin(client):
#     client.post("/sign-up", data={"email":"test@gmail.com", "username":"admin", "password1":"admin", "password2":"admin"})
#     client.post("/login", data={"email":"test@gmail.com","password":"admin"})
#     response = client.get("/admin")
#     assert b"This user does not have admin access." in response.data
    


def test_users(client):
    client.post("/sign-up", data={"email":"test@gmail.com", "username":"admin", "password1":"admin", "password2":"admin"})
    client.post("/login", data={"email":"test@gmail.com","password":"admin"})
    response = client.get("/users")
    assert b"Admin Portal" in response.data


def test_professor_created(client):
    response = client.post("/sign-up", data={"email":"prof1@gmail.com", 
                                  "username":"prof1", 
                                  "password1":"professor", 
                                  "password2":"professor", 
                                  "role":"Professor",
                                  "professor_token" :"123"
                                  }, follow_redirects=True)
    assert b"User Created as Professor" in response.data
    
def test_create_exercise(client):
    client.post("/sign-up", data={"email":"prof1@gmail.com", 
                                  "username":"prof1", 
                                  "password1":"professor", 
                                  "password2":"professor", 
                                  "role":"Professor",
                                  "professor_token" :"123"
                                  })
    client.post("/login", data={"email":"prof1@gmail.com","password":"professor"}, follow_redirects=True)

    data={"title": "abc",
        "description" : "def",
        "solution" : "hello",
        "countdown" : "10",
        }
    
    data['descriptionfile'] = (io.BytesIO(b"abcdef"), 'test.jpg')

    response = client.post("/create-exercise", data=data, follow_redirects=True,       
                                                content_type='multipart/form-data')
    assert b"Exercise created!" in response.data


def test_student_created(client):
    response = client.post("/sign-up", data={"email":"stud1@gmail.com", 
                                  "username":"stud1", 
                                  "password1":"student", 
                                  "password2":"student", 
                 
                                  }, follow_redirects=True)

    assert b"User Created as Student" in response.data


    # client.post("/login", data={"email":"stud1@gmail.com","password":"student"}, follow_redirects=True)
    
    # data={"title": "abc",
    #     "description" : "def",
    #     "solution" : "hello",
    #     "countdown" : "10",
    #     }
    
    # data['descriptionfile'] = (io.BytesIO(b"abcdef"), 'test.jpg')

    # response = client.post("/create-exercise", data=data, follow_redirects=True,       
    #                                             content_type='multipart/form-data')
    # assert b"Exercise created!" in response.data

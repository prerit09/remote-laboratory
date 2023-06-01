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


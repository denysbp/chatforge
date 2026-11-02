from app.models import User

PASSWORD = "123456"

def test_invalid_password() -> None:
    user = User()
    user.password_hash = PASSWORD
    assert user.authenticate(PASSWORD[::-1]) ==  False

def test_valid_password() -> None:
    user = User()
    user.password_hash = PASSWORD
    assert user.authenticate(PASSWORD) == True
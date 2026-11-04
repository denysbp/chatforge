from app.models import (
    User,
    Conversation,
    Message,
    RefreshToken
)
from sqlalchemy.orm import Session
from app.enviroment import Enviroment
from app.core import DataBase

PASSWORD = "123456"
connection = DataBase()
connection.create_tables()
session: Session = connection.get_session()



def test_store_models() -> None:
    user = User(
        name="Test",
        email="test@example.com"
    )
    user.password_hash = PASSWORD

    con = Conversation(
        title="TEST",
        author=user
    )

    mess = Message(
        conversation=con
    )

    session.add(user)
    session.commit()

    stored_message = session.query(Message).filter_by(
        conversation_id=con.id
    ).first()

    assert stored_message is not None
    assert stored_message.conversation_id == con.id



def test_invalid_password() -> None:
    user = User()
    user.password_hash = PASSWORD
    assert user.authenticate(PASSWORD[::-1]) ==  False

def test_valid_password() -> None:
    user = User()
    user.password_hash = PASSWORD
    assert user.authenticate(PASSWORD) == True
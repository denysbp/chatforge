from app.models import (
    User,
    Conversation,
    Message,
    RefreshToken
)
from app.enviroment import Enviroment
from app.core import Connection

PASSWORD = "123456"
connection = Connection()
connection.create_tables()
Session = connection.get_session()
session = Session()


def test_store_models() -> None:
    user = User()
    con = Conversation(
        user_id=user.id,
        title="TEST",
    )
    mess = Message(
        conversation_id=con.id,
    )
    user.chats.append(con)
    session.add(user)
    session.add(con)
    session.add(mess)
    session.commit()

    assert session.query(Message).filter_by(con.id) == con.id


def test_invalid_password() -> None:
    user = User()
    user.password_hash = PASSWORD
    assert user.authenticate(PASSWORD[::-1]) ==  False

def test_valid_password() -> None:
    user = User()
    user.password_hash = PASSWORD
    assert user.authenticate(PASSWORD) == True
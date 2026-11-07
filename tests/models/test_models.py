from chat-app.models import (
    User,
    Conversation,
    Message,
)
from sqlalchemy.orm import Session, close_all_sessions
from chat-app.core import DataBase
import pytest

PASSWORD = "123456"
connection = DataBase()
session: Session = connection.get_session()

try:
    @pytest.fixture(scope="session", autouse=True)
    def setup_database():
        connection.create_tables()

        yield

        connection.drop_tables()

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
finally:
    connection.close()
    close_all_sessions()
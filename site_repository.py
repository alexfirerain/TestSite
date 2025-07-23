from data.db_session import create_session
from data.user_model import User
from data.consideration_model import Consideration
from data.pic_model import Picture


def get_user_by_id(user_id: int) -> User | None:
    with create_session() as db_sess:
        return db_sess.query(User).get(user_id)


def get_user_by_email(email: str) -> User | None:
    with create_session() as db_sess:
        return db_sess.query(User).filter(User.email == email).first()


def save_user(user: User) -> bool:
    try:
        with create_session() as db_sess:
            db_sess.add(user)
            db_sess.commit()
        return True
    except Exception as e:
        print(f"Ошибка при сохранении пользователя: {e}")
        return False


def update_user(user: User) -> bool:
    try:
        with create_session() as db_sess:
            existing_user = db_sess.query(User).get(user.id)
            if not existing_user:
                raise ValueError("Нет такого пользователя")

            existing_user.name = user.name
            existing_user.email = user.email
            existing_user.about = user.about
            db_sess.commit()
        return True
    except Exception as e:
        print(f"Ошибка при обновлении пользователя: {e}")
        return False


def delete_user_by_id(user_id: int) -> bool:
    try:
        with create_session() as db_sess:
            user = db_sess.query(User).get(user_id)
            if not user:
                raise ValueError("Нет такого пользователя")
            db_sess.delete(user)
            db_sess.commit()
        return True
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")
        return False


def get_all_users() -> list[User]:
    with create_session() as db_sess:
        return db_sess.query(User).all()


def get_all_public_considerations() -> list[Consideration]:
    with create_session() as db_sess:
        return db_sess.query(Consideration).filter(Consideration.is_private == False).all()


def get_considerations_by_user(user_id: int) -> list[Consideration]:
    with create_session() as db_sess:
        return db_sess.query(Consideration).filter(Consideration.author == user_id).all()


def get_pictures_by_user(user_id: int) -> list[Picture]:
    with create_session() as db_sess:
        return db_sess.query(Picture).filter(Picture.owner == user_id).all()

def save_picture(user_id: int, filename: str) -> bool:
    try:
        with create_session() as db_sess:
            picture = Picture(
                filename=filename,
                user_id=user_id
            )
            db_sess.add(picture)
            db_sess.commit()
        return True
    except Exception as e:
        print(f"Ошибка внесения картинки в БД: {e}")
        return False
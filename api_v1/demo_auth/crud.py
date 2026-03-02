from users.schemas import UserSchema
from auth import utils as auth_utils

john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@mail.ru",
)
sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}

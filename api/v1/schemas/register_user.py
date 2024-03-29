from crud.schemas import User, UserCreate


class RegisterUserRequest(UserCreate):
    pass


class RegisterUserResponse(User):
    pass

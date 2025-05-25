import falcon
import falcon.asgi
from domain.user import User
from dataclasses import asdict
from adapters.dynamodb import DynamoDBRepository


class RegisterUserResource:
    def __init__(self, repository: DynamoDBRepository):
        self.repository = repository

    async def on_post(self, req: falcon.asgi.Request, resp: falcon.asgi.Response):
        """Method to perform register on user"""
        payload: dict = await req.get_media()
        new_user: User = (
            User(email=payload["email"], password=payload["password"])
            .validate_clear_password()
            .hash_password()
        )

        if await self.repository.get_user(new_user) is not None:
            resp.media = {"message":"There is already a user with this emal"}
            resp.status = falcon.HTTP_400

        await self.repository.create_user(new_user)
        resp.media = asdict(new_user)
        resp.status = falcon.HTTP_201
        return resp


class LoginUserResource:
    def __init__(self, repository: DynamoDBRepository) -> None:
        self.repository = repository

    async def on_post(self, req: falcon.asgi.Request, resp: falcon.asgi.Response):
        """Method to perform login for user"""
        payload: dict = await req.get_media()
        try:
            existing_user: User = await self.repository.get_user(
                user=User(email=payload["email"], password=payload["password"])
            )
        except Exception as e:
            print(e)

        if existing_user is None:
            resp.media = {"message": "Invalid email"}
            resp.status = falcon.HTTP_400

        elif existing_user.verify_password(password=payload["password"]) is False:
            """
            Password entered if incorrect
            """
            resp.media = {"message": "Invalid password"}
            resp.status = falcon.HTTP_400
        else:
            resp.media = asdict(existing_user)
            resp.status = falcon.HTTP_201

        return resp

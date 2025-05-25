import falcon
import falcon.asgi
import uvicorn

from adapters.dynamodb import DynamoDBRepository
from adapters.errors import AdapterError
from api.handlers import handle_adapter_error, handle_domain_validation_error
from api.resources import LoginUserResource, RegisterUserResource
import config
from domain.errors import DomainValidationError

if __name__ == "__main__":
    app = falcon.asgi.App()
    repository: DynamoDBRepository = DynamoDBRepository(
        table_name=config.DYNAMODB_TABLE_NAME,
        endpoint_url=config.DYNAMODB_URL,
        region=config.DYNAMODB_REGION,
    )

    user_register_resource: RegisterUserResource = RegisterUserResource(
        repository=repository
    )

    user_login_resource: LoginUserResource = LoginUserResource(repository=repository)

    app.add_route("/api/v1/register", user_register_resource)
    app.add_route("/api/v1/login", user_login_resource)

    app.add_error_handler(DomainValidationError, handle_domain_validation_error)
    app.add_error_handler(AdapterError, handle_adapter_error)

    host = "localhost"
    port = 8080
    uvicorn.run(app, host=host, port=port)

import falcon
import falcon.asgi

from domain.errors import DomainValidationError


async def handle_domain_validation_error(
    req: falcon.asgi.Request,
    resp: falcon.asgi.Response,
    ex: DomainValidationError,
    params,
) -> None:
    """Falcon error handler for managing domain validation errors"""
    raise falcon.HTTPBadRequest(
        title = "Domain validation error",
        code = "INVALID FIELD",
        description = ex.message
    )

async def handle_adapter_error(
    req: falcon.asgi.Request,
    resp: falcon.asgi.Response,
    ex: DomainValidationError,
    params,
) -> None:
    """Falcon error handler for managing adapter errors"""
    raise falcon.HTTPError(
        title = "Adapter Error",
        code = "500", # maybe get the code from ex
        description = ex.message
    )
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Optional

from adapters.errors import AdapterError
from domain.user import User
from aioboto3.session import Session
from types_aiobotocore_dynamodb.service_resource import Table
from logging import Logger

logger: Logger = Logger(__name__)


class DynamoDBRepository:
    def __init__(
        self,
        session: Optional[Session] = None,
        table_name: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        region: Optional[str] = None,
    ):
        self.session: Session = session or Session()
        self.table_name: str = table_name
        self.endpoint_url: str = endpoint_url
        self.region: str = region

    @asynccontextmanager
    async def dynamo_table(self) -> AsyncGenerator[Table, Any]:
        """Context manager for DynamoDb table resource."""
        try:
            async with self.session.resource(
                service_name="dynamodb",
                endpoint_url=self.endpoint_url,
                region_name=self.region,
            ) as db_resource:
                table = await db_resource.Table(self.table_name)
                table.get_item
                yield table

        except Exception as e:
            logger.error(
                "Error accessing DynamoDB table %s: %s.",
                self.table_name,
                e,
                exc_info=True,
            )
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            logger.error(
                "DynamoDB ClientError accessing table '%s': Code: %s, Message: %s",
                self.table_name,
                error_code,
                error_message,
                exc_info=True,
            )
            extra: dict[str, Any] = {
                "error_type": "AdapterError._name_",
                "table_name": self.table_name,
                "original_error_message": str(e),
                "original_error_type": "type(e)._name_",
            }

            if error_code == "ResourceNotFoundException":
                logger.error(
                    f"DynamoDB table '{self.table_name}' not found. Ensure the table exists and is correctly configured.",
                    extra=extra,
                    exc_info=True,
                )
                raise AdapterError(
                    message=f"DynamoDB table '{self.table_name}' not found."
                ) from e
            elif error_code == "ProvisionedThroughputExceededException":
                logger.error(
                    f"Provisioned throughput exceeded for DynamoDB table '{self.table_name}'. Consider increasing the provisioned capacity or using on-demand mode.",
                    extra=extra,
                    exc_info=True,
                )
                raise AdapterError(
                    message="Provisioned throughput exceeded for DynamoDB"
                    f"table '{self.table_name}'."
                ) from e
            elif error_code == "ConditionalCheckFailedException":
                logger.error(
                    f"Conditional check failed for DynamoDB table '{self.table_name}'. The document does not match the expected version or condition.",
                    extra=extra,
                    exc_info=True,
                )
                raise AdapterError(
                    message="Conditional check failed, document doesn't match version"
                ) from e
            else:
                logger.error(
                    f"Unexpected DynamoDB error occurred for table '{self.table_name}': {error_message}.",
                    extra=extra,
                    exc_info=True,
                )
                raise AdapterError(
                    message=f"Unexpected DynamoDB error: {error_message}."
                ) from e

    async def create_user(self, user: User) -> None:
        """
        Creates a new user in dynamodb
        """
        dynamodb_user: dict[str | str] = {
            "PK": f"USER#{user.email}",
            "SK": "METADATA",
            "PASSWORD": user.password,
        }

        async with self.dynamo_table() as table:
            await table.put_item(
                Item=dynamodb_user,
                ConditionExpression="attribute_not_exists(PK) AND attribute_not_exists(SK)",
            )

    async def get_user(self, user: User) -> User | None:
        """
        Get a user from dynamodb
        """
        async with self.dynamo_table() as table:
            result = await table.get_item(
                Key={
                    "PK": f"USER#{user.email}",
                    "SK": "METADATA",
                }
            )
            if result.get("Item",None) is None:
                return None

        return User(
            email=result["Item"]["PK"].split("#")[1],
            password=result["Item"]["PASSWORD"],
        )
    
    async def get_all_users(self):
        # TODO: to finish
        async with self.dynamo_table() as table:
            table.query(
                
            )
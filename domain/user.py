import re
import bcrypt
from domain.errors import DomainValidationError
import dataclasses


@dataclasses.dataclass
class User:
    """
    Represents a user on the application.
    """
    email: str = ""
    password: str = "" # holds the hashed password
    
    def __post_init__(self) -> "None":
        """
        Post init(after the User object is created, perform some validations/processing)
        """
        self._validate()

    def _validate(self):
        """
        Method to validate the fields
        """
        errors: list[Exception] = []

        for validation_function in [self._validate_email]:
            try:
                validation_function()
            except DomainValidationError as error:
                errors.append(error)

        if errors:
            raise DomainValidationError(
                "Validation failed: " + "; ".join(str(e.message) for e in errors)
            )

    def hash_password(self) -> "User":
        """Method to hash the password"""
        self.password = bcrypt.hashpw(self.password.encode(), bcrypt.gensalt()).decode()
        return self

    def validate_clear_password(self) -> "User":
        """
        Method to validate password
        """
        if not self.password:
            raise DomainValidationError(message="Missing password")
        if len(self.password) < 8:
            raise DomainValidationError(message="Password too short")
        # if parola este asemanatoare cu email ##
        #     raise DomainValidationError(message="")
        
        return self

    def _validate_email(self):
        """
        Method to validate password
        """
        if not self.email:
            # Check for the email to be present
            raise DomainValidationError(message="Missing email.")

        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, self.email) is None:
            # Check for the email to be an actual email.
            raise DomainValidationError(message="Wrong email format")

    def verify_password(self,password:str) -> bool:
        """Method to check if the password for this user is corect"""
        return bcrypt.checkpw(password.encode(),self.password.encode())
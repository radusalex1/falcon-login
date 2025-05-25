# from domain.errors import DomainValidationError


# try:
#     raise DomainValidationError(message="1234")
# except DomainValidationError as error:
#     print(error)

import bcrypt

hash = bcrypt.hashpw("RaduAlexandru(2001)#".encode(), bcrypt.gensalt()).decode()
print(hash)
print(bcrypt.checkpw("RaduAlexandru(2001)#".encode(),hash.encode()))
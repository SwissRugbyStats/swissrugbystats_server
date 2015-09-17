from rest_framework.exceptions import APIException


class ResourceAlreadyExists(APIException):
    status_code = 409
    default_detail = 'The resource you wanted to create already exists.'
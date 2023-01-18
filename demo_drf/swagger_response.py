from drf_yasg import openapi

from demo_drf.response_example import login_response_example, change_password_response_example

api_signup = {
    "200": openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="username of user",
                ),
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="E-mail id of user",
                ),
            },
        ),
    )
}

api_login = {
    "200": openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="refresh token to get access token",
                ),
                "access": openapi.Schema(
                    type=openapi.TYPE_STRING,

                    description="access token for authorization",
                ),
                "user": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="username of user",
                ),
                "id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="id of user",
                ),
            },
        ),
        examples=login_response_example,
    )
}

api_change_password = {
    "200": openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="New password that is to be changed",
                ),
                "password2": openapi.Schema(
                    type=openapi.TYPE_STRING,

                    description="Password2 field that match new password field",
                ),
                "old_password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Old password of User ",
                ),
            },
        ),
        examples=change_password_response_example,
    )
}
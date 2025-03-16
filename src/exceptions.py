from fastapi import status, Request, Response
from fastapi.responses import JSONResponse


class UniqueConstraintError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def unique_constraint_handler(request: Request, exception: UniqueConstraintError) -> Response:
    _, attribute = exception.msg.split(': ')
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": f"Database entry already exists: attribute={attribute}."}
    )

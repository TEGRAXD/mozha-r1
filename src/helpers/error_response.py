from src.models import schemas

def error_response_models():
    return {
        400: {"model": schemas.ErrorResponse},
        403: {"model": schemas.ErrorResponse},
        404: {"model": schemas.ErrorResponse},
        422: {"model": schemas.ErrorResponse},
        500: {"model": schemas.ErrorResponse},
    }

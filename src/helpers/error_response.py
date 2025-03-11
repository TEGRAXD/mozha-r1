from typing import Dict
from fastapi.responses import JSONResponse

def custom_error_response(status_code: int, status: str, message: str, error: dict[str, any]):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status,
            "message": message,
            "error": error,
        }
    )
from fastapi.responses import JSONResponse

def success_response(message: str, data=None, status_code: int = 200):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "success",
            "message": message,
            "data": data
        }
    )

def error_response(message: str, error=None, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
            "error": error
        }
    )

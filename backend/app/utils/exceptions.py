from fastapi import HTTPException, status


class AuthInvalidError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="인증 정보가 올바르지 않습니다")


class AuthLockedError(HTTPException):
    def __init__(self, minutes_remaining: int):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"계정이 잠겨있습니다. {minutes_remaining}분 후 재시도해주세요",
        )


class AuthExpiredError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰이 만료되었습니다")


class ForbiddenError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="접근 권한이 없습니다")


class NotFoundError(HTTPException):
    def __init__(self, resource: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{resource}을(를) 찾을 수 없습니다")


class DuplicateError(HTTPException):
    def __init__(self, resource: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=f"이미 존재하는 {resource}입니다")


class NoActiveSessionError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="활성 세션이 없습니다")

from fastapi import APIRouter, Depends, HTTPException
from app.exception import UserNotCorrectPasswordException, UserNotFoundException
from app.users.auth.service import AuthService
from app.dependecy import get_auth_service
from app.users.user_profile.schema import UserCreateSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    body: UserCreateSchema, auth_service: AuthService = Depends(get_auth_service)
):
    try:
        result = await auth_service.login(body.username, body.password)
        return result
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)

    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)

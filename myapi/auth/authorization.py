from myapi.config import SECRET_KEY, ALGORITHM
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

# OAuth2 for different user roles
student_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/student/login/verify-otp")
staff_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/staff/login/verify-otp")

# Common function to decode JWT for any role
def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_identity = payload.get("sub")
        user_role = payload.get("role")# `sub` contains phone number (or email for students)

        if user_identity is None:
            raise credentials_exception
        return {"id":user_identity, "role":user_role}

    except JWTError:
        raise credentials_exception

# Role-based authentication
def get_current_student(token: str = Depends(student_oauth2_scheme)):
    return get_current_user(token)

def get_current_worker(token: str = Depends(staff_oauth2_scheme)):
    return get_current_user(token)

# this file will handle the authentication of the user
# it will handle the login, logout, and registration of the user
# it will also handle the forgot password and reset password
# it will also handle the change password
# it will also handle the user verification
# it will also handle the user email verification

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional


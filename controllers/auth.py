import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Optional

# Configuración de la clave secreta y el algoritmo para JWT
SECRET_KEY = "edfgdfrrd"  # Cambia esto por una clave secreta más segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tiempo de expiración del token

# Contexto para encriptar contraseñas con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer para manejar la extracción del token desde las cabeceras de autorización
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Función para crear el token de acceso
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar el token JWT
def verify_token(token: str):
    try:
        # Decodificamos el token con la clave secreta y el algoritmo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Devuelve el payload que contiene los datos del usuario
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token no válido o expirado")

# Dependencia que extrae y verifica el usuario autenticado a partir del token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)  # Verificamos el token
    if payload is None:
        raise HTTPException(status_code=401, detail="Token no válido o expirado")
    return payload  # Devuelve el payload con los datos del usuario (por ejemplo, el email)

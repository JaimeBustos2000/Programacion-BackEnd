import jwt
from ninja.security import HttpBearer
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone

SECRET_KEY = "InAcAp2024"

def generar_token(user):
    payload = {
        "user_id": user.id,
        "group_id": "admin_products",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def validar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # El token expiró
    except jwt.InvalidTokenError:
        return None  # Token inválido


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        payload = validar_token(token)
        if not payload:
            return None
        try:
            return User.objects.get(id=payload["user_id"])
        except User.DoesNotExist:
            return None
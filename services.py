import secrets
from fastapi.exceptions import HTTPException
from starlette.middleware.authentication import AuthenticationError
from entities import (UserModel, Token, ContatoRequest,
                      ContatoResponse, ContatoModel)


def create_user(**kwargs) -> UserModel:
    user: UserModel = UserModel.create(**kwargs)
    password = kwargs.get('password')
    if password:
        user.set_password(password)
        user.save()
    return user


def get_token(username, password) -> Token:
    try:
        user: UserModel = UserModel.get(UserModel.username == username)
    except UserModel.DoesNotExist:
        raise HTTPException(status_code=404)
    if not user.check_password(password):
        raise HTTPException(status_code=401)
    user.token = secrets.token_hex()
    user.save()
    credential = Token(token=user.token)
    return credential


def create_contato(contato: ContatoRequest) -> ContatoResponse:
    contato_doc = ContatoModel(retorno=contato.retorno,
                               texto=contato.texto,
                               user=contato.user)
    contato_doc.save()
    return ContatoResponse(**contato_doc.__data__)


def check_user_token(token) -> UserModel:
    try:
        user: UserModel = UserModel.get(UserModel.token == token)
    except UserModel.DoesNotExist:
        raise AuthenticationError('User does not exist.')
    return user

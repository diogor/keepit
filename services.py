import secrets
from .entities import (UserModel, Token, ContatoRequest,
                       ContatoResponse, ContatoModel)

def create_user(**kwargs) -> UserModel:
    user: UserModel = UserModel.create(**kwargs)
    password = kwargs.get('password')
    if password:
        user.set_password(password)
        user.save()
    return user


def get_token(username, password) -> Token:
    user: UserModel = UserModel.get(UserModel.username == username)
    if not user.check_password(password):
        raise GraphQLError('Permissão negada.')
    user.token = secrets.token_hex()
    user.save()
    credential = Token(token=user.token)
    return credential


def create_contato(contato: ContatoRequest) -> ContatoResponse:
    contato_doc = ContatoModel(retorno=contato.retorno, texto=contato.texto)
    contato_doc.save()
    return contato

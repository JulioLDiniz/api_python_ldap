import ldap
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from classes.usuarios_input import UsuarioInput
from jose import jwt, JWTError
from fastapi import status
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from datetime import datetime
from decouple import config
from datetime import timedelta

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

crypt_context = CryptContext(schemes=['sha256_crypt'])

app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello':'World'}

@app.post('/auth2')
def user_login():
    #VERIFICAR SE USUÁRIO EXISTE
    #FOO
    usuario = 'euler'
    senha = crypt_context.hash('password')
    

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválidas!'
        )
    if not crypt_context.verify('password', senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválidas!'
        )
    
    exp = datetime.now() + timedelta(minutes=30)

    payload = {
        'sub' : usuario,
        'exp' : exp
    }

    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        'access_token': access_token,
        'exp': exp
     }
    

@app.post('/auth')
def acesso_ldap(inputs: UsuarioInput) -> str:
    """
    Faz a conexão com o servidor LDAP e retorna se o usuário/senha são válidos
    A base LDAP utilizada é a do site: https://www.forumsys.com/2022/05/10/online-ldap-test-server/
    """
    try:
        ldap_conn = ldap.initialize('ldap://ldap.forumsys.com')
    except ldap.SERVER_DOWN:
        return "Não foi possível se conectar com o servidor LDAP!"
    try:
        retorno = ldap_conn.simple_bind_s(f'uid={inputs.usuario},dc=example,dc=com', f'{inputs.senha}')
        if(retorno):
            return 'Usuário conectado com sucesso!'
        else:
            return 'Usuário não encontrado'
    except ldap.INVALID_CREDENTIALS:
        return 'This password is incorrect!'


# if __name__ == '__main__':
#     uvicorn.run(app, port=8000)






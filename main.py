import ldap
import sys
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from classes.usuarios_input import UsuarioInput

app = FastAPI()

@app.get('/')
def read_root():
    return {'Hello':'World'}


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
        texto = ldap_conn.simple_bind_s(f'uid={inputs.usuario},dc=example,dc=com', f'{inputs.senha}')
        return 'Usuário conectado com sucesso!'
    except ldap.INVALID_CREDENTIALS:
        return 'This password is incorrect!'


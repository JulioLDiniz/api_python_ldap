
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
from pprint import pprint
from classes.ldap_access import LDAPAccess

from classes.model.usuario_model import UsuarioModel

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

crypt_context = CryptContext(schemes=['sha256_crypt'])

app = FastAPI()

@app.post('/auth')
def user_login(inputs: UsuarioInput, expires_in: int = 30):
    
    
    usuario = inputs.usuario
    senha = crypt_context.hash(inputs.senha)
    
    acesso_ldap = LDAPAccess.acesso_ldap(inputs)
    

    if acesso_ldap['status'] == False and acesso_ldap['code'] != 1:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
            {
                'status_code':status.HTTP_401_UNAUTHORIZED,
                'msg':'Credenciais inválidas!'
            }
        )
    if acesso_ldap['status'] == True and acesso_ldap['code'] == 1:
        exp = datetime.now() + timedelta(minutes=30+expires_in)

        payload = {
            'sub' : usuario,
            'exp' : exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        usuarioTK = UsuarioModel()
        usuarioTK.criar_token(access_token, usuario)
        return {
            'access_token': access_token,
            'exp': exp
        }    
    


# if __name__ == '__main__':
#     uvicorn.run(app, port=8000)






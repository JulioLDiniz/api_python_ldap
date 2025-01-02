from pydantic import BaseModel

class UsuarioInput(BaseModel):
    usuario: str
    senha: str

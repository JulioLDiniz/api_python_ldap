import ldap
from classes.usuarios_input import UsuarioInput

class LDAPAccess:
    def acesso_ldap(inputs: UsuarioInput) -> str:
        """
        Faz a conexão com o servidor LDAP e retorna se o usuário/senha são válidos
        A base LDAP utilizada é a do site: https://www.forumsys.com/2022/05/10/online-ldap-test-server/
        
        STATUS CÓDIGO DE RETORNO:
        1 = OK
        2 = NÃO FOI POSSÍVEL SE CONECTAR COM O SERVIDOR
        3 = USUÁRIO NÃO ENCONTRADO
        4 = CREDENCIAIS INVÁLIDAS
        
        """
        try:
            ldap_conn = ldap.initialize('ldap://ldap.forumsys.com')
        except ldap.SERVER_DOWN:
            return {
                'msg' : 'Não foi possível se conectar com o servidor LDAP!',
                'code' : 2,
                'status': False
            }
        try:
            retorno = ldap_conn.simple_bind_s(f'uid={inputs.usuario},dc=example,dc=com', f'{inputs.senha}')
            if(retorno):
                return {
                    'msg' : 'Usuário conectado com sucesso!',
                    'code' : 1,
                    'status': True
                }
            else:
                return {
                    'msg' : 'Usuário não encontrado!',
                    'code' : 3,
                    'status': False
                }
        except ldap.INVALID_CREDENTIALS:
            return {
                'msg' : 'Credenciais inválidas!',
                'code' : 4,
                'status': False   
            }
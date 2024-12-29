import ldap
import sys

try:
    ldap_conn = ldap.initialize('ldap://ldap.forumsys.com')
except ldap.SERVER_DOWN:
    print("Can't contact LDAP server")
    exit(4)
try:
    texto = ldap_conn.simple_bind_s('uid=boyle,dc=example,dc=com', 'password')
    print(texto[0])
    print('Usuário conectado com sucesso!')
except ldap.INVALID_CREDENTIALS:
    print("This password is incorrect!")
    sys.exit(3)


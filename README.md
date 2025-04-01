# api_python_ldap
API REST para autenticação com LDAP utilizando python-ldap e FastAPI.

Surgiu de uma ideia de aproveitar um servidor de autenticação que utiliza SAMBA para unificar os usuários de uma empresa permitindo que haja um login único em diversos sistemas (AD/Login da máquina e sistemas web).

Consiste em:

1 - Fazer a conexão com o servidor LDAP (https://www.forumsys.com/2022/05/10/online-ldap-test-server/);
2 - Verificar se o usuário e senha do servidor LDAP está válido. Caso não esteja, retorna um erro 401 informando que as credenciais estão inválidas; e 
3 - Caso seja válido, cria um token JWT com validade para 30 minutos.


Sugestão de melhoria: 

- Criar um endpoint para revogação de token; e
- Criar uma verificação de grupos para permitir que somente determinado usuário tenha acesso a determinado sistema.
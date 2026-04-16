# Database Setup (SQL Server Docker)

## Arquivos

- `01_init_database.sql`: cria o banco `access_system`.
- `03_create_schema.sql`: cria tabela `dbo.users` e índice.
- `02_create_app_user.sql`: cria login/usuário da aplicação com privilégio mínimo na tabela `users`.
- `04_verify.sql`: valida estrutura e lista usuários.
- `scripts.sql`: bootstrap único (banco + schema) para setup rápido.

## Execução recomendada (sqlcmd)

No host, usando o container já publicado em `localhost,1433`:

```powershell
docker exec -i sql_server_container /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "<SA_PASSWORD>" -C -i /dev/stdin < database/01_init_database.sql
docker exec -i sql_server_container /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "<SA_PASSWORD>" -C -i /dev/stdin < database/03_create_schema.sql
docker exec -i sql_server_container /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "<SA_PASSWORD>" -C -v APP_PASSWORD="<APP_PASSWORD>" -i /dev/stdin < database/02_create_app_user.sql
docker exec -i sql_server_container /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "<SA_PASSWORD>" -C -i /dev/stdin < database/04_verify.sql
```

## Importante

- Não salvar senha em `login.txt` ou arquivo versionado.
- Passe segredos por variável de ambiente/comando.
- No backend, use o login da aplicação (ex.: `access_app`) em vez de `sa`.

## Seed de administrador

O admin deve ser criado via backend para garantir hash bcrypt:

```powershell
cd backend
flask --app run.py seed-admin --username admin --password "Admin@123456"
```

:setvar DB_NAME access_system
:setvar APP_LOGIN access_app
:setvar APP_PASSWORD ChangeMe_StrongPassword_123!

/*
Run with sqlcmd so variables work:
sqlcmd -S localhost,1433 -U sa -P "<SA_PASSWORD>" -C -i database/02_create_app_user.sql -v APP_PASSWORD="<NEW_PASSWORD>"
*/

IF NOT EXISTS (SELECT 1 FROM sys.sql_logins WHERE name = N'$(APP_LOGIN)')
BEGIN
    DECLARE @create_login_sql NVARCHAR(MAX);
    SET @create_login_sql =
        N'CREATE LOGIN [' + REPLACE(N'$(APP_LOGIN)', N']', N']]') +
        N'] WITH PASSWORD = N''' + REPLACE(N'$(APP_PASSWORD)', N'''', N'''''') +
        N''', CHECK_POLICY = ON, CHECK_EXPIRATION = OFF;';
    EXEC (@create_login_sql);
END
GO

DECLARE @grant_sql NVARCHAR(MAX);
SET @grant_sql = N'
USE [' + REPLACE(N'$(DB_NAME)', N']', N']]') + N'];

IF NOT EXISTS (SELECT 1 FROM sys.database_principals WHERE name = N''' + REPLACE(N'$(APP_LOGIN)', N'''', N'''''') + N''')
BEGIN
    CREATE USER [' + REPLACE(N'$(APP_LOGIN)', N']', N']]') + N'] FOR LOGIN [' + REPLACE(N'$(APP_LOGIN)', N']', N']]') + N'];
END;

GRANT SELECT, INSERT, UPDATE, DELETE ON dbo.users TO [' + REPLACE(N'$(APP_LOGIN)', N']', N']]') + N'];
';

EXEC (@grant_sql);
GO

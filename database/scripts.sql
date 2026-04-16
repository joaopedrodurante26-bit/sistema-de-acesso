IF DB_ID('access_system') IS NULL
BEGIN
    CREATE DATABASE access_system;
END
GO

USE access_system;
GO

IF OBJECT_ID('dbo.users', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(80) NOT NULL UNIQUE,
        password_hash NVARCHAR(128) NOT NULL,
        role NVARCHAR(10) NOT NULL DEFAULT 'USER',
        is_active BIT NOT NULL DEFAULT 1,
        created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        CONSTRAINT ck_users_role CHECK (role IN ('ADMIN', 'USER'))
    );

    CREATE INDEX ix_users_username ON dbo.users(username);
END
GO

/*
Admin seed is done via Flask CLI to keep bcrypt hashing in application layer:

    cd backend
    flask --app run.py seed-admin --username admin --password "Admin@123456"
*/

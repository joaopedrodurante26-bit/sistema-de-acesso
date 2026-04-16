/*
Bootstrap script for local development.

This script creates:
1) database: access_system
2) schema/table: dbo.users

For application login/user creation with least privilege, run:
    database/02_create_app_user.sql

Admin seed remains in application layer (bcrypt):
    cd backend
    flask --app run.py seed-admin --username admin --password "Admin@123456"
*/

IF DB_ID(N'access_system') IS NULL
BEGIN
    CREATE DATABASE access_system;
END
GO

USE access_system;
GO

IF OBJECT_ID(N'dbo.users', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(80) NOT NULL UNIQUE,
        password_hash NVARCHAR(255) NOT NULL,
        role NVARCHAR(10) NOT NULL CONSTRAINT df_users_role DEFAULT 'USER',
        is_active BIT NOT NULL CONSTRAINT df_users_is_active DEFAULT 1,
        created_at DATETIME2(0) NOT NULL CONSTRAINT df_users_created_at DEFAULT SYSUTCDATETIME(),
        updated_at DATETIME2(0) NOT NULL CONSTRAINT df_users_updated_at DEFAULT SYSUTCDATETIME(),
        CONSTRAINT ck_users_role CHECK (role IN ('ADMIN', 'USER'))
    );
END
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = N'ix_users_username' AND object_id = OBJECT_ID(N'dbo.users')
)
BEGIN
    CREATE INDEX ix_users_username ON dbo.users(username);
END
GO

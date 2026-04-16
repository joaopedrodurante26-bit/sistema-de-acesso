USE access_system;
GO

SELECT name AS table_name
FROM sys.tables
WHERE name = N'users';
GO

SELECT name AS index_name
FROM sys.indexes
WHERE object_id = OBJECT_ID(N'dbo.users') AND name = N'ix_users_username';
GO

SELECT TOP 20 id, username, role, is_active, created_at, updated_at
FROM dbo.users
ORDER BY id;
GO

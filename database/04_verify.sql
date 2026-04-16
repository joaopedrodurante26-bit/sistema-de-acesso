USE access_system;
GO

SELECT name AS table_name
FROM sys.tables
WHERE name = N'users';
GO

SELECT kc.name AS unique_constraint_name
FROM sys.key_constraints kc
WHERE kc.parent_object_id = OBJECT_ID(N'dbo.users')
  AND kc.type = 'UQ';
GO

SELECT TOP 20 id, username, role, is_active, created_at, updated_at
FROM dbo.users
ORDER BY id;
GO

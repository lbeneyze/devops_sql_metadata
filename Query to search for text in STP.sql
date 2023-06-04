SELECT DISTINCT
s.name
, o.name AS Object_Name
, o.type_desc
FROM sys.sql_modules m
INNER JOIN sys.objects o
ON m.object_id = o.object_id
INNER JOIN sys.schemas s
ON s.schema_id= o.schema_id
WHERE m.definition Like '%DTI1011511_Orders%'
--where s.name = 'omagen'
--and o.type_desc = 'SQL_STORED_PROCEDURE'
order by 1,2,3;


select t.[schema_name], t.sp_name, sum(t.lines_of_code) - 1 as lines_ofcode, t.type_desc
from
(
    select o.name as sp_name, 
	stp.[schema_name],
    (len(c.text) - len(replace(c.text, char(10), ''))) as lines_of_code,
    case when o.xtype = 'P' then 'Stored Procedure'
    when o.xtype in ('FN', 'IF', 'TF') then 'Function'
    end as type_desc

    from sysobjects o

    inner join syscomments c
    on c.id = o.id
  
	left outer join 
	(
		SELECT SCHEMA_NAME([schema_id]) as [schema_name],
		name
		FROM sys.procedures
	) stp
	on stp.name = o.name

    where o.xtype in ('P', 'FN', 'IF', 'TF')
	and stp.[schema_name] = 'omagen'
    and o.category = 0
    and o.name not in ('fn_diagramobjects', 'sp_alterdiagram', 'sp_creatediagram', 'sp_dropdiagram', 'sp_helpdiagramdefinition', 'sp_helpdiagrams', 'sp_renamediagram', 'sp_upgraddiagrams', 'sysdiagrams')
) t
where t.sp_name like '%_TF_sa_%'
group by t.[schema_name], t.sp_name, t.type_desc
order by 3 

POSTGRES_QUERY = """
    SELECT 
        cols.table_schema,
        cols.table_name,
        cols.column_name,
        cols.is_nullable,
        cols.data_type,
        pgd.description AS column_comment
    FROM information_schema.columns AS cols
    LEFT JOIN pg_catalog.pg_statio_all_tables AS st ON 
        cols.table_schema = st.schemaname 
        AND cols.table_name = st.relname
    LEFT JOIN pg_catalog.pg_description AS pgd ON 
        pgd.objoid = st.relid 
        AND pgd.objsubid = cols.ordinal_position
    WHERE cols.table_schema = '{schema}'
    ORDER BY cols.table_name, cols.ordinal_position
"""


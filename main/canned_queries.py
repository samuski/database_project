from django.db import connection

canned_queries = {}

def register_query(func):
    """Decorator to save to canned_queries."""
    canned_queries[func.__name__] = func
    return func

# TODO We are not actually enforcing not null?
@register_query
def create_table_ref():
    query="""
        CREATE TABLE ref_table (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        name STRING NOT NULL,
        number INTEGER
        )
    """
    chart_type = "none"
    return query, chart_type

@register_query
def create_table_main():
    query="""
        CREATE TABLE main_table (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        name STRING,
        ref_id INTEGER,
        FOREIGN KEY (ref_id) REFERENCES ref_table (id)
        )
    """
    chart_type = "none"
    return query, chart_type

@register_query
def create_table_people():
    query="""
        CREATE TABLE people (
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        user_id STRING,
        first_name STRING,
        last_name STRING,
        sex STRING,
        email STRING,
        phone STRING,
        birthdate STRING,
        job_title STRING  
    );
    """
    chart_type = "none"
    return query, chart_type

@register_query
def create_table_million_i():
    query="""
        CREATE TABLE million_i (
        col1 INTEGER PRIMARY KEY AUTO_INCREMENT,
        col2 INTEGER
        )
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def select_all_people():
    query="""
        select * from people
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def select_all_main():
    query="""
        select * from main_table
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def copy_people():
    query="""
        COPY people FROM 'people_100k.csv'
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def copy_million_i():
    query="""
        COPY million_i FROM 'million_i.csv'
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def index_people():
    query="""
        CREATE INDEX idx_people ON people (first_name, last_name)
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def join_main_ref():
    query="""
        select * from main_table join ref_table on main_table.ref_id = ref_table.id
    """
    chart_type = "bar"
    return query, chart_type
@register_query
def drop_table_ref():
    query="""
        DROP TABLE ref_table
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def drop_table_main():
    query="""
        DROP TABLE main_table
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def drop_table_people():
    query="""
        DROP TABLE people
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def drop_table_million_i():
    query="""
        DROP TABLE million_i
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def query_people0():
    query="""
        SELECT job_title, COUNT(*) AS total
        FROM people
        WHERE job_title LIKE 'E%'
        GROUP BY job_title
        Order by total DESC
        LIMIT 10
    """
    chart_type = "bar"
    return query, chart_type
@register_query
def query_people1():
    query="""
        SELECT job_title, COUNT(*) AS total
        FROM people
        GROUP BY job_title
        ORDER BY total DESC
        HAVING total < 190
        LIMIT 10
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def query_people2():
    query="""
        SELECT first_name, last_name, birthdate
        FROM people
        WHERE birthdate < '1980-01-01'
        ORDER BY birthdate DESC
    """
    chart_type = "bar"
    return query, chart_type

@register_query
def query_people3():
    query="""
        SELECT sex, COUNT(*) AS total
        FROM people
        GROUP BY sex
    """
    chart_type = "heatmap"
    return query, chart_type

@register_query
def query_people4_slow():
    query="""
        #SELECT a.first_name AS person1, b.first_name AS person2, a.job_title
        FROM people AS a
        JOIN people AS b ON a.job_title = b.job_title
        WHERE a.id < b.id
        LIMIT 10
    """
    chart_type = "heatmap"
    return query, chart_type

@register_query
def single_aggregates():
    query="""
        SELECT SUM(col1), MIN(col1), MAX(col2), AVG(col1), COUNT(*) from million_i
    """
    chart_type = "bar"
    return query, chart_type

# TODO The column names are off again.
@register_query
def lmx1000_join():
    query = """
        SELECT *  from million_i as t1 join thousand_i t2 on t1.col1 = t2.col1
    """
    chart_type = "pie"
    return query, chart_type

# TODO We don't support dot inside of aggregates.
@register_query
def join_aggregates():
    query = """
        SELECT SUM(t1.col1), MIN(t2.col1), MAX(t1.col2), AVG(t.2col1), COUNT(*) from million_i as t1 join thousand_i t2 on t1.col1 = t2.col1
    """
    chart_type = "pie"
    return query, chart_type

@register_query
def insert_main():
    query = """
        INSERT INTO main_table (name, ref_id) VALUES ("Sam",1)
    """
    chart_type = "pie"
    return query, chart_type

@register_query
def insert_ref():
    query = """
        INSERT INTO ref_table (name, number) VALUES ("DBMS", 1)
    """
    chart_type = "pie"
    return query, chart_type

@register_query
def update_main():
    query = """
        UPDATE main_table SET name = "Wisdom" WHERE name = "Sam"
    """
    chart_type = "pie"
    return query, chart_type

@register_query
def delete_main():
    query = """
        DELETE FROM ref_table WHERE number = 1
    """
    chart_type = "pie"
    return query, chart_type
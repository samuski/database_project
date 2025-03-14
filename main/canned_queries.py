from django.db import connection

canned_queries = {}

def register_query(func):
    """Decorator to save to canned_queries."""
    canned_queries[func.__name__] = func
    return func


# def execute_query(query):
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         results = cursor.fetchall()
#         columns = [col[0] for col in cursor.description]
#     return results, columns


# 1. Monthly Crime Trends in Both Cities
@register_query
def monthly_trends():
    query="""
        SELECT 
            l.city,
            to_char(date_trunc('month', t.crimetime), 'Month') AS month,
            COUNT(*) AS crime_count
        FROM crime c
        JOIN location l ON c.locationid = l.locationid
        JOIN timeinfo t ON c.timeid = t.timeid
        GROUP BY l.city, to_char(date_trunc('month', t.crimetime), 'Month')
        ORDER BY l.city, month; 
    """
    chart_type = "bar"
    return query, chart_type

# 2. Most Common Types of Crime by City
@register_query
def common_crime():
    query="""
        SELECT 
            l.city,
            ct.crimedesc,
            COUNT(*) AS count_crimes
        FROM crime c
        JOIN location l ON c.locationid = l.locationid
        JOIN crimetype ct ON c.crimetypeid = ct.crimetypeid
        GROUP BY l.city, ct.crimedesc
        ORDER BY l.city, count_crimes DESC;
    """
    chart_type = "bar"
    return query, chart_type

# 3. Areas with Highest Arrest Rate
@register_query
def high_arrest():
    query="""
        SELECT 
            l.city,
            l.area,
            SUM(CASE WHEN c.arrestmade THEN 1 ELSE 0 END) AS arrests,
            COUNT(*) AS total_crimes,
            ROUND(100.0 * SUM(CASE WHEN c.arrestmade THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percentage
        FROM crime c
        JOIN location l ON c.locationid = l.locationid
        GROUP BY l.city, l.area
        ORDER BY arrest_rate_percentage DESC;
    """
    chart_type = "bar"
    return query, chart_type

# 4. Peak Hours
@register_query
def peak_hours():
    query="""
        SELECT 
            EXTRACT(HOUR FROM t.crimetime) AS hour,
            COUNT(*) AS crime_count
        FROM crime c
        JOIN timeinfo t ON c.timeid = t.timeid
        GROUP BY hour
        ORDER BY hour;
    """
    chart_type = "bar"
    return query, chart_type

# 5. Peak Days
@register_query
def peak_days():
    query="""
        SELECT 
            to_char(t.crimetime, 'Day') AS day_of_week,
            COUNT(*) AS crime_count
        FROM crime c
        JOIN timeinfo t ON c.timeid = t.timeid
        GROUP BY day_of_week
        ORDER BY crime_count DESC;
    """
    chart_type = "bar"
    return query, chart_type

# 6. Geographical Crime Hotspots
@register_query
def hotspots():
    query="""
        SELECT 
            l.latitude,
            l.longitude,
            COUNT(*) AS crime_count
        FROM crime c
        JOIN location l ON c.locationid = l.locationid
        GROUP BY l.latitude, l.longitude
        ORDER BY crime_count DESC
        LIMIT 50;
    """
    chart_type = "bar"
    return query, chart_type

# 7. Year-over-Year Crime Rate Changes
@register_query
def yoy_crime():
    query="""
        WITH yearly AS (
            SELECT 
              EXTRACT(YEAR FROM t.crimetime) AS year,
              COUNT(*) AS crime_count
            FROM crime c
            JOIN timeinfo t ON c.timeid = t.timeid
            GROUP BY year
            ORDER BY year
          )
          SELECT 
              year,
              crime_count,
              LAG(crime_count) OVER (ORDER BY year) AS previous_year_count,
              ROUND(100.0 * (crime_count - LAG(crime_count) OVER (ORDER BY year)) / NULLIF(LAG(crime_count) OVER (ORDER BY year), 0), 2) AS percent_change
          FROM yearly;
    """
    chart_type = "bar"
    return query, chart_type

# 8. Crime Type Distribution by City District
@register_query
def crime_district():
    query="""
        SELECT 
            l.city,
            l.area,
            ct.crimedesc,
            COUNT(*) AS crime_count
        FROM crime c
        JOIN location l ON c.locationid = l.locationid
        JOIN crimetype ct ON c.crimetypeid = ct.crimetypeid
        GROUP BY l.city, l.area, ct.crimedesc
        ORDER BY l.city, l.area, crime_count DESC;
    """
    chart_type = "bar"
    return query, chart_type

# 9. Seasonal Crime Pattern
@register_query
def crime_season():
    query="""
        SELECT 
          season,
          COUNT(*) AS crime_count
        FROM (
          SELECT 
            CASE 
              WHEN EXTRACT(MONTH FROM t.crimetime) IN (3,4,5) THEN 'Spring'
              WHEN EXTRACT(MONTH FROM t.crimetime) IN (6,7,8) THEN 'Summer'
              WHEN EXTRACT(MONTH FROM t.crimetime) IN (9,10,11) THEN 'Fall'
              WHEN EXTRACT(MONTH FROM t.crimetime) IN (12,1,2) THEN 'Winter'
            END AS season
          FROM crime c
          JOIN timeinfo t ON c.timeid = t.timeid
          -- Optionally add a WHERE clause to filter by a specific year or range
        ) sub
        GROUP BY season
        ORDER BY
          CASE 
            WHEN season = 'Winter' THEN 1
            WHEN season = 'Spring' THEN 2
            WHEN season = 'Summer' THEN 3
            WHEN season = 'Fall' THEN 4
          END;
    """
    chart_type = "line"
    return query, chart_type

# 10. Sliding Weekly Pattern by Type 
@register_query
def crime_slide():
    query="""
        WITH daily_counts AS (
          SELECT
            ct.crimedesc,
            date(t.crimetime) AS crime_date,
            COUNT(*) AS daily_count
          FROM crime c
          JOIN timeinfo t ON c.timeid = t.timeid
          JOIN crimetype ct ON c.crimetypeid = ct.crimetypeid
          WHERE t.crimetime >= current_date - interval '1 year'
          GROUP BY ct.crimedesc, date(t.crimetime)
        ),
        moving_stats AS (
          SELECT
            crimedesc,
            crime_date,
            daily_count,
            AVG(daily_count) OVER (PARTITION BY crimedesc ORDER BY crime_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7,
            STDDEV(daily_count) OVER (PARTITION BY crimedesc ORDER BY crime_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS sd_7
          FROM daily_counts
        )
        SELECT
          crimedesc,
          crime_date,
          daily_count,
          ma_7,
          sd_7,
          ROUND((daily_count - ma_7) / NULLIF(sd_7, 0), 2) AS z_score
        FROM moving_stats
        ORDER BY crimedesc, crime_date;
    """
    chart_type = "bar"
    return query, chart_type
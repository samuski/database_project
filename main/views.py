import os
import glob
import json
import decimal 

from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from main.data_files.init_database import table_init, load_tables
from main.canned_queries import canned_queries

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def is_data_imported():
    table_init() # Error proofed with IF NOT EXISTS
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM crime;")
        count = cursor.fetchone()[0]
    return count > 0


def execute_query(query, page, per_page=30):
    with connection.cursor() as cursor:
        cursor.execute(query)
        if cursor.description:
            raw_results = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
        else:
            return None, None
        # Paginate the results
        paginator = Paginator(raw_results, per_page)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        return results, columns

def graph(results):
    if not results:
        return {}
    # Assume each row contains two values: an x-axis label and a y-axis numeric value.
    labels = [row[0] for row in results]
    try:
        values = [float(row[1]) for row in results]
    except Exception:
        values = [row[1] for row in results]
    return {
        "labels": labels,
        "datasets": [{
            "label": "Incident Count",  # You can change this label as needed.
            "data": values,
            "backgroundColor": "rgba(54, 162, 235, 0.6)",
            "borderColor": "rgba(54, 162, 235, 1)",
            "borderWidth": 1
        }]
    }

def dashboard(request):

    # if not is_data_imported():
    #     master_file = None
    #     csv_files = glob.glob(os.path.join(BASE_DIR, "data_files", "*.csv"))
    #     for csv_file in csv_files:
    #         if csv_file == "/app/main/data_files/crime.csv":
    #             master_file = csv_file
    #         else:
    #             load_tables(csv_file)
    #     load_tables(master_file) # Goes last due to all the foreign relations involved.
    # else:
    #     print("Data already imported, skipping.")

    results = None
    columns = None
    error_message = None
    success_message = None
    graph_data = None
    chart_type = None

    query = request.GET.get("sql_query", "")
    page = request.GET.get("page", 1)

    if request.method == "POST":
        page = 1
        # New query submitted, clear previous one
        query = request.POST.get("sql_query", "")
        request.session["last_query"] = query  # Store query in session

        canned_query = request.POST.get("canned_query" "")

        if canned_query and canned_query in canned_queries:
            query, chart_type = canned_queries[canned_query]()
            results, columns = execute_query(query, page)
            graph_data = graph(results)
        if query:
            request.session["last_query"] = query

    elif "last_query" in request.session:
        # Preserve query across pagination clicks
        query = request.session["last_query"]
    if query:
        try:
            results, columns = execute_query(query, page)
            if results is None:
                success_message = "Query executed successfully."
            else:
                graph_data = json.dumps(graph(results), default=lambda o: float(o) if isinstance(o, decimal.Decimal) else o)

        except Exception as e:
            error_message = str(e)
            results = None
            columns = None

    return render(request, "dashboard.html", {
        "results": results,
        "columns": columns if results else None,
        "error_message": error_message,
        "success_message": success_message,
        "query": query,
        "graph_data" : graph_data,
        "chart_type": chart_type
    })
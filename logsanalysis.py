#!/usr/bin/env python

import psycopg2
from datetime import date
import dateutil.parser

db = psycopg2.connect("dbname=news user=postgres host=127.0.0.1 password=postgres port=5432")
c = db.cursor()
query = """
        with top_paths as (
            select substring (path, 10) as slug, count(*) as num
            from log
            where status = '200 OK'
            group by path
            )
        select articles.title, top_paths.num
        from articles, top_paths
        where articles.slug = top_paths.slug
        order by num desc
        limit 3;
        """
c.execute(query)
rows = c.fetchall()

print("\nQuestion 1: What are the most popular three articles of all time?\n")

for i in rows:
    print("'{s[0]}' - {s[1]} views".format(s=i))

query = """
        with paths as (
            select substring (path, 10) as slug
            from log
            where status = '200 OK'
        )
        select authors.name, count(*) as num 
        from authors, articles, paths
        where authors.id = articles.author and articles.slug = paths.slug
        group by authors.name 
        order by num desc;
        """
c.execute(query)
rows = c.fetchall()

print("\nQuestion 2: Who are the most popular article authors of all time?\n")

for i in rows:
    print("'{s[0]}' - {s[1]} views".format(s=i))

query = """
        select date_trunc('day', time)::date as day,
            round(sum(case when status != '200 OK' then 1 end)::numeric / count(status) * 100, 2) as "% errors"
        from log
        group by day
        order by "% errors" desc
        limit 1;
        """
c.execute(query)
rows = c.fetchall()

date = rows[0][0].strftime("%B %d, %Y")
error_percent = rows[0][1]

print("\nQuestion 3: On which days did more than 1% of requests lead to errors?\n")

print("{} - {}% errors\n".format(date, error_percent))
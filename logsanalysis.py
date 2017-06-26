#!/usr/bin/env python

"""used to connect to a database"""
import psycopg2

# Connect to the docker database
db = psycopg2.connect("dbname=news user=postgres host=127.0.0.1 password=postgres port=5432")
c = db.cursor()

# Query for question 1: What are the most popular three articles of all time?
# Make a temp 'top_paths' table with just the slug portion of the path and only where there were no errors
# and combine that with the articles table on the slug to get the article name
# order by the num count descending and only show the top 3
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

print"\nQuestion 1: What are the most popular three articles of all time?\n"

# Loop through results and format them for readability
for i in rows:
    print"'{s[0]}' - {s[1]} views".format(s=i)

# Query for question 2: Who are the most popular article authors of all time?
# Make a temp 'paths' table with just the slug portion of the path and only where there were no errors
# Then combine the temp paths table with the author's table that has the id we need to join the with 
# the articles table for the slug. group up by the authors name, count it, and sort it descending
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

print"\nQuestion 2: Who are the most popular article authors of all time?\n"

# Loop through results and format them for readability
for i in rows:
    print"'{s[0]}' - {s[1]} views".format(s=i)

# Query for question 3: On which days did more than 1% of requests lead to errors?
# group the time stamps by the day by truncating the time and setting that as 'day'
# count the errors with a sum of a case statement that assigns a 1 to every error and set it to a numeric value
# then divide that by the total count of all hits for that day and shift the decimal then round for a readable %
# order by the highest errors percentage and only show the top result 
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

# take date result and convert it to written out date
date = rows[0][0].strftime("%B %d, %Y")
error_percent = rows[0][1]

print"\nQuestion 3: On which days did more than 1% of requests lead to errors?\n"

# Print answer and format for readability
print"{} - {}% errors\n".format(date, error_percent)

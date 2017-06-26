#!/usr/bin/env python

import psycopg2

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

print("'{s[0][0]}' - {s[0][1]} views".format(s=rows))

# [
#     ('Candidate is jerk, alleges rival', 338647L),
#     ('Bears love berries, alleges bear', 253801L),
#     ('Bad things gone, say good people', 170098L)
# ]

# for i in rows:
#     print(i[0])
#     print(i[1])

# print()



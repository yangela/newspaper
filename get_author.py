## This scripts uses the Python package Newspaper, an article scraping & curation
## library, to scrape the author name of specific articles when provided with the URL.
## The author name is then stored in the corresponding SQL table.

from mysqldb import db
from contextlib import closing
from newspaper import Article

with closing(db.cursor()) as cur:
    cur.execute("""
    select URL from db.table1 where
    Author IS NULL
    """)
    rows = cur.fetchall()
    for record in rows:
        url = record[0]
        try:
            a = Article(url=url, language='en', fetch_images=False)
            a.download()
            a.parse()
            keyperson = a.authors
            keyperson_str = ', '.join(keyperson)
            print keyperson_str
            except Exception as e:
            print e

        cur.execute("""
        UPDATE db.table1 SET Author = %s WHERE URL = %s
        """, (keyperson_str, url))
        db.commit()

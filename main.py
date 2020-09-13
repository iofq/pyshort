from flask import Flask, request, render_template, redirect
import base64
from math import floor
import string
import sqlite3
from urllib.parse import urlparse

base_64 = string.digits + string.ascii_lowercase + string.ascii_uppercase

app = Flask(__name__)
host = "https://s.iofq.net/"

def to_base64(num, b = 62):
    r = num % b
    result = base_64[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        result = base_64[int(r)] + result
    return result

def to_base10(num, b = 62):
    result = 0
    for i in range(len(num)):
        result = b * result + base_64.find(num[i])
    return result


def table_check():
    create_table = """
        CREATE TABLE WEB_URL(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        URL TEXT NOT NULL
        );
        """
    with sqlite3.connect('url.db') as db:
        cursor = db.cursor()
        try:
            cursor.execute(create_table)
        except sqlite3.OperationalError as e:
            print(e)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        og_url = str.encode(request.form.get("url"))
        if urlparse(og_url).scheme == '':
            url = 'http://' + og_url
        else:
            url = og_url
        with sqlite3.connect('url.db') as db:
            cursor = db.cursor()
            result = cursor.execute(
                    'INSERT INTO WEB_URL (URL) VALUES (?)', [base64.urlsafe_b64encode(url)]
            )

            db.commit()
            encoded = to_base64(result.lastrowid)

        return render_template('home.html', short_url=host + encoded)
    return render_template('home.html')

@app.route('/<short_url>', methods=['GET'])
def redirect_short(short_url):
    decoded = to_base10(short_url)
    url = host  #fallback

    try: 
        with sqlite3.connect('url.db') as db:
            cursor = db.cursor()
            result = cursor.execute('SELECT URL FROM WEB_URL WHERE ID=?', [decoded])
            try:
                short = result.fetchone()
                if short is not None:
                    url = base64.urlsafe_b64decode(short[0])
                    
            except Exception as e:
                print(e)
        url = url.decode("utf-8")
        if urlparse(url).scheme == '':
            url = 'http://' + url
        print(url)
        return redirect(url)
    except Exception as e:
        print("no short url found", e)

    except OverflowError as e:
        print(str(e))

if __name__ == '__main__':
    table_check()
    app.run(host='0.0.0.0', debug=True)
    

from github_webhook import Webhook
from flask import Flask
from flask_mysqldb import MySQL


# Config
MYSQL_HOST = 'galera-lb.mysql'
MYSQL_USER = 'qmk'
MYSQL_PASSWORD = 'qmk'
MYSQL_DB = 'qmk_bot'
MYSQL_USE_UNICODE = True
MYSQL_CURSORCLASS = 'DictCursor'

# Setup
app = Flask(__name__)
app.config.from_object(__name__)
github_secret = None
webhook = Webhook(app, '/postreceive', github_secret)
print(' * MySQL Host:%s User:%s DB:%s' % (app.config['MYSQL_HOST'],
                                          app.config['MYSQL_USER'],
                                          app.config['MYSQL_DB']))
mysql = MySQL(app)


# MySQL functions
def get_cursor():
    return mysql.connection.cursor()


def commit():
    return mysql.connection.commit()


def query(sql, *args):
    """Returns data from the database.
    """
    curs = get_cursor()
    curs.execute(sql, args)
    return curs.fetchall()


def update_row(table, primary_key_column, primary_key_value, **column_values):
    """Updates a single row in a table inside MySQL.
    """
    value_placeholders = ['%s = %%s' % i for i in column_values]
    sql = "UPDATE %s SET %s WHERE %s = %%s" % (table,
                                               ', '.join(value_placeholders),
                                               primary_key_column)
    args = list(column_values.values())
    args.append(primary_key_value)

    results = query(sql, args)
    commit()

    return results


# Views
@app.route("/")
def index():
    return "Hello, World!"


@app.route("/healthcheck")
def healthcheck():
    return "GOOD"


@webhook.hook('push')
def on_push(data):
    """Handle a webhook from github.
    """
    print('Got webhook request:')
    print(data)
    query('INSERT INTO requests (request_text, request_repr) VALUE (%s, %s)',
          str(data), repr(data))

from flask_cors import CORS
import pymysql
from flaskext.mysql import MySQL
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "" #provide a secret key
CORS(app)

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = '' # Specify Endpoint
app.config['MYSQL_DATABASE_USER'] = '' # Specify Master username
app.config['MYSQL_DATABASE_PASSWORD'] = '' # Specify Master password
app.config['MYSQL_DATABASE_DB'] = '' # Specify database name

mysql.init_app(app)

def list_create(SQL):
    labels = []
    data = []
    try:
        conn = mysql.connect() 
        cursor = conn.cursor(pymysql.cursors.DictCursor) 
        cursor.execute(SQL) 
        empRows = cursor.fetchall()
        
    except Exception as e:
        print(e)
        
    finally:
        cursor.close() 
        conn.close()
        
    for i in empRows[0].keys():
        labels.append(i) # Get the column names
        data.append(empRows[0][i]) # Get the values of the columns

    return labels, data

@app.route('/')
def home():
    SQL = "SELECT y2015, y2016, y2017, y2018, y2019, y2020 FROM city_rents WHERE city = 'New York'"
    labels_ny, data_ny = list_create(SQL)
    
    SQL = "SELECT y2015, y2016, y2017, y2018, y2019, y2020 FROM city_rents WHERE city = 'Chicago'"
    labels_cg, data_cg = list_create(SQL)
  
    return render_template("chartjs.html", data_ny=data_ny, labels_ny=labels_ny, data_cg=data_cg)
        
if __name__ == "__main__":
    app.run()

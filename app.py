#setup dependencies
import numpy as np
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from config import password


#Database setup:
protocol = 'postgresql'
host = 'localhost'
port = 5432
database_name = 'yahoo_stock_db'
rds_connection_string = f'{protocol}://postgres:{password}@{host}:{port}/{database_name}'
engine = create_engine(rds_connection_string)
conn = engine.connect()

#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

# Flask setup
app = Flask(__name__)

#Flask Routes:

#creating homepage:
@app.route("/")
def homepage():
    return render_template("index.html")

#creating /api/
@app.route ("/stocks_list")
def stocks_list():
    # retrieve data from postgresql database
    data_sql= pd.read_sql_query('select * from stocks', con=engine)

    #convert list of tuples into normal list
    stocks_data_list = list(np.ravel(data_sql))
    #convert to json
    stock_data = jsonify(stocks_data_list)
    return render_template("stock_list.html", myData=stock_data)

@app.route ("/stockdata")
def stockdata():
    #retrieve_data = session.query().all()
    retrieve_stock = pd.read_sql_query("SELECT * FROM stocks", conn)
    # retrieve_stock.set_index('dat', inplace=True)
    result = {}

    #set a loop to iterate the whole table
    for index,row in retrieve_stock.iterrows():
        result[index]= dict(row)
    
    #convert to json
    return jsonify(result)

if __name__ == '__main__':
    app.run (debug=True)
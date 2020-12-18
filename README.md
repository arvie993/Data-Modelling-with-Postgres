## Introduction


Sparkify has some data from their music streaming app that needs to be analyzed  
They specifically look into the songs that user are listening. At present ehty have only the data of the user activity and the songs as JSON format in the app. 

In this project. We will crate a Postgres database to fullfill the needs of the analists to query the databases consist of a schema and the tables in it. 
While accomplising this project we will also test the expectations of the analizing team's queries in the given query tables. 

Our database schema will be star schema with **one fact table** (songplays) and **four dimension tables** (users, songs, artists, time).

## sql_queries.py

To create the database tables and insert the data the **sql_queries.py** files is utilized. Each table mentioned above is created and the insert statements are added in  the same file. To repatedly test the project to make sure it is working properly we added drop statements as well.

## Create_tables.py & test.ipynb

We run **cerate_tables.py** on terminal to successfully complete the tables in our database. **Test.ipynb** is utilized to test if the all necessary tables are created. All select clauses in the test.ipynb should bring empty tables when run for the first level.

## etl.ipynb

We develop ETL processes for each table in the **etl.ipynb**. The necessary data from the JSON files are filtered and inserted to the tables with the proecss performed for each table in this notebook.  At the end of each table section, or at the end of the notebook, we run **test.ipynb** to confirm that records were successfully inserted into each table. Reruning **create_tables.py** is crucial to reset tables before each time we run this notebook.

## etl.py

The process we created in **etl.ipynb** notebook will be used for the ultimate pipeline to create and insert the data to the tables. The iterations in this file will use the process created and insert each JSON files to the related table in our database. 

Finally we can rerun the test.ipynb to make sure the data is successfully insertted to the tables. 

![](images/diagram.png)

## How to Run the Python Scripts

We first start to create our tables with crate_tables.py. We run this script in terminal with **python create_tables.py** command. This create our tables and make ready to insert our JSON files. Then we run our second scprint  with **python etl.py**. This run the functions we have in the etl.py file and add each JSON file to the correct table. Finaly we can run test.ipynb notebook to see if the data is correctly inserted to each table.


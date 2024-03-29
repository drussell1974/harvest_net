
PYTHON
------

## use yarn to add requirement.txt to active virtual environment

> sudo apt-get install python3.10-distutils

> sudo apt-get install python3-apt

1. Use 'apt-get install --reinstall package-name', if necessary.

> sudo apt-get install build-essential libssl-dev libffi-dev python-dev

> pip install -r requirements.txt


SQLITE
------

https://www.sqlite.org/quickstart.html
https://www.sqlitetutorial.net/sqlite-python/
https://www.sqlite.org/datatype3.html

> sudo apt install sqlite3

> mkdir sqlite

> cd sqlite

# open the SQLITE database

> sqlite3 ./test.db


## Extracting data from sqlite for analysis


> .headers ON
> .output harvestnet_data.csv
> SELECT d.run_id, r.begin_date as run_date, d.order_of_result, r.customer_id, r.search_terms, r.category, d.product_id, d.product_code, d.product_name, d.lead_date, d.lead_days, d.in_stock, d.price, d.discount FROM run r INNER JOIN web_scraping d ON r.id = d.run_id;

# Upload the data to to Harvest Net 

*For ChatGPT to analyse, the maximum file size is 512MB.*

1. Go to https://chat.openai.com/g/g-ZLI3KFo0s-harvest-net
2. Upload the data
3. The data should be sent as ordered in the search.




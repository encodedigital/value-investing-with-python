import requests
import psycopg2

#ENTER YOUR PostgreSQL PASSWORD IN BELOW CONNECTION STRING
conn = psycopg2.connect(database="stocks-us", user = "postgres", password = "xxxxxxxx", host = "127.0.0.1", port = "5432")

def insertData(f_data):
    try:
        sql = "INSERT INTO tickers (stock, stock_name, current_price, exchange) VALUES (%s,%s,%s,%s)"
        data = f_data
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
    except Exception as e:
        print(e)

def main():
    try:
        url = "https://financialmodelingprep.com/api/v3/company/stock/list"

        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

        response = requests.get(url, headers={'User-Agent': ua})

        for data in response.json()["symbolsList"]:
            try:
                if((data["exchange"] == "Nasdaq Global Select" or data["exchange"] == "New York Stock Exchange") and data["price"] > 10):
                    f_data = [data["symbol"], data["name"], data["price"], data["exchange"]]
                    insertData(f_data)
                    print(f_data)
            except Exception as e:
                continue
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

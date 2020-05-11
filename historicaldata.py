import requests
import psycopg2
import json


conn = psycopg2.connect(database="stocks-us", user = "postgres", password = "encodedigital", host = "127.0.0.1", port = "5432")

def insertData(f_data):
        sql = "INSERT INTO financials (stock, income_statement, balance_sheet, cash_flow, enterprise_value, key_metrics, financial_growth) VALUES (%s,%s,%s,%s,%s,%s,%s)" 
        data = f_data
        cursor = conn.cursor()
        cursor.execute(sql,data)
        conn.commit()
        cursor.close()

def main():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

    cur = conn.cursor()
    cur.execute("select stock from tickers;")
    rows = cur.fetchall()

    for row in rows:
        try:
            table = row[0]
            url = "https://financialmodelingprep.com/api/v3/financials/income-statement/"+table     
            response = requests.get(url, headers={'User-Agent': ua})
            income_statement = json.dumps(response.json())

            url = "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/"+table     
            response = requests.get(url, headers={'User-Agent': ua})
            balance_sheet = json.dumps(response.json())

            url = "https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/"+table     
            response = requests.get(url, headers={'User-Agent': ua})
            cash_flow = json.dumps(response.json())

            url = "https://financialmodelingprep.com/api/v3/enterprise-value/"+table     
            response = requests.get(url, headers={'User-Agent': ua})
            enterprise_value = json.dumps(response.json())

            url = "https://financialmodelingprep.com/api/v3/company-key-metrics/"+table     
            response = requests.get(url, headers={'User-Agent': ua})
            key_metrics = json.dumps(response.json())

            url = "https://financialmodelingprep.com/api/v3/financial-statement-growth/"+table     
            response = requests.get(url, headers={'User-Agent': ua})
            financial_growth = json.dumps(response.json())

            f_data = [table, income_statement, balance_sheet, cash_flow, enterprise_value, key_metrics, financial_growth] 

            insertData(f_data)
            print("Printed: ", table)

        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    main()
import pandas as pd

from arraymanipulation import total_sum

product = ["Apples","Bannas","Oranges","Grapes","Pineapples"]

sales = [150,200,180,90,60]

sales_series = pd.Series(sales, index=product)


print(sales_series)

print(sales_series['Grapes'])

total_sum
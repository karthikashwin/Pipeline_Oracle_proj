import cx_Oracle
import pandas as pd
import matplotlib.pyplot as plt

dsn = cx_Oracle.makedsn(
    host="obiwan.gre.ac.uk",
    port=1521,
    service_name="obiwan.gre.ac.uk"
)

connection = cx_Oracle.connect(
    user="sg5928s",
    password="sg5928s",
    dsn=dsn
)

print("Connected.")

# --- 1. FACT TABLE ROW COUNT ---
df_count = pd.read_sql("SELECT COUNT(*) AS total_rows FROM FACT_DAILY_PERF", connection)
display(df_count)


# --- 2. TOP 10 EDITIONS BY GROSS MARGIN ---
sql = """
SELECT p.title, SUM(f.gross_margin) AS total_gross_margin
FROM FACT_DAILY_PERF f
JOIN DIM_PRODUCT p ON f.product_key = p.product_key
GROUP BY p.title
ORDER BY total_gross_margin DESC
FETCH FIRST 10 ROWS ONLY
"""
df_top = pd.read_sql(sql, connection)
display(df_top)

!pip install seaborn

import seaborn as sns

# --- HEATMAP QUERY ---
sql_heat = """
SELECT p.title, c.channel_name, SUM(f.units_sold) AS units_sold
FROM FACT_DAILY_PERF f
JOIN DIM_PRODUCT p ON f.product_key = p.product_key
JOIN DIM_CHANNEL c ON f.channel_key = c.channel_key
GROUP BY p.title, c.channel_name
"""

df_heat = pd.read_sql(sql_heat, connection)

# Pivot data for heatmap
pivot = df_heat.pivot(index='TITLE', columns='CHANNEL_NAME', values='UNITS_SOLD')

# Plot heatmap
plt.figure(figsize=(12,6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues")
plt.title("Heatmap: Units Sold by Edition & Channel")
plt.show()

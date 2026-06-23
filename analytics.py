import sqlite3
import matplotlib.pyplot as plt


conn = sqlite3.connect("medvision.db")
cursor = conn.cursor()

cursor.execute("""
SELECT disease, COUNT(*)
FROM predictions
GROUP BY disease
""")

data = cursor.fetchall()

conn.close()

labels = [row[0] for row in data]
values = [row[1] for row in data]

plt.figure(figsize=(8,5))
plt.bar(labels, values)

plt.title("Disease Distribution")
plt.xlabel("Disease")
plt.ylabel("Predictions")

plt.savefig("static/charts/disease_chart.png")
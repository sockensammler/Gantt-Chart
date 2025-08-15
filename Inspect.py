import inspect
from highcharts_gantt.chart import Chart

# Alle Attribute und Methoden des Chart-Objekts auflisten
chart = Chart()
all_attrs = dir(chart)

print("\n--- Alle Attribute / Methoden von Chart ---")
for attr in all_attrs:
    print(attr)

print("\n--- Methoden mit Signatur ---")
for name, func in inspect.getmembers(chart, inspect.ismethod):
    print(f"{name}{inspect.signature(func)}")


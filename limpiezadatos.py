from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

csv_path = Path(__file__).with_name("loan_data.csv")
df = pd.read_csv(csv_path)


#Tabla de de impago por proposito
default_rate_by_purpose = (
    df.groupby("purpose")["not.fully.paid"].mean().mul(100).sort_values()
)

ax = default_rate_by_purpose.plot(kind="barh", figsize=(10, 6)) 
ax.set(
    title="Tasa de préstamos no pagados por propósito",
    xlabel="Préstamos no pagados (%)",
    ylabel="Propósito del préstamo",
)
ax.figure.tight_layout()
plt.show()

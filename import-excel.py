import pandas as pd
from sqlalchemy import create_engine
import sys

# read in the excel data dump, ignoring the crap in the frist 4 rows
df = pd.read_excel(sys.argv[1], skiprows=4)

# connect to our DB
engine = create_engine("postgresql://@/chris")

# rewrite the columb headers to match our DB
df2 = df.rename(
    columns={
        "update time": "updatetime",
        "PV1 voltage (V)": "voltpv1",
        "PV1 current (A)": "amppv1",
        "PV1 input power(W)": "wattpv1",
        "PV2 voltage (V)": "voltpv2",
        "PV2 current (A)": "amppv2",
        "PV2 input power(W)": "wattpv2",
        "AC voltage (V)": "voltac",
        "AC current(A)": "ampac",
        "output power(W)": "wattac",
        "AC Power (W)": "wattac",
        "feed-in power(W)": "wattexport",
        "daily yield(kWh)": "dayyeild",
        "total yield(kWh)": "totalyield",
        "feed-in energy(kWh)": "feedin",
        "consume energy(kWh)": "consumed",
        "Inverter Status": "status",
    }
)

# convert our timestamp to a datetime
df2["updatetime"] = pd.to_datetime(df2["updatetime"])

# make our new data time the index
df2.set_index("updatetime", inplace=True)

# append it to our DB
df2.to_sql("solar_generation", engine, if_exists="append")

# print the date of the first/last entry in this file
print("start: " + str(df2.index[0].date()))
print("end: " + str(df2.index[-1].date()))

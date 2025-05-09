import pandas as pd
from sqlalchemy import create_engine
import sys

# read in the excel data dump, ignoring the crap in the frist 4 rows
df = pd.read_excel(sys.argv[1], skiprows=4)
#only now its only 1 row... so suppor that too
if all(not str(col).startswith("PV") for col in df.columns):
    df = pd.read_excel(sys.argv[1], skiprows=1)

# connect to our DB
engine = create_engine("postgresql://@/chris")

# make column names lowercase first
df.columns = df.columns.str.lower()
# rewrite the column headers to match our DB
df2 = df.rename(
    columns={
        "update time": "updatetime",
        "pv1 voltage (v)": "voltpv1",
        "pv1 current (a)": "amppv1",
        "pv1 input power(w)": "wattpv1",
        "pv1 power (w)": "wattpv1",
        "pv2 voltage (v)": "voltpv2",
        "pv2 current (a)": "amppv2",
        "pv2 input power(w)": "wattpv2",
        "pv2 power (w)": "wattpv2",
        "ac voltage (v)": "voltac",
        "ac voltage l (v)": "voltac",
        "ac current(a)": "ampac",
        "ac current l (a)": "ampac",
        "output power(w)": "wattac",
        "ac power (w)": "wattac",
        "ac power l (w)": "wattac",
        "daily yield(kwh)": "dayyeild",
        "daily inverter output (kwh)": "dayyeild",
        "total yield(kwh)": "totalyield",
        "total inverter output (kwh)": "totalyield",
        "inverter status": "status",
        "inverter statue": "status",
        "mppt1 voltage (v)": "voltpv1",
        "mppt1 current (a)": "amppv1",
        "mppt1 power (w)": "wattpv1",
        "mppt2 voltage (v)": "voltpv2",
        "mppt2 current (a)": "amppv2",
        "mppt2 power (w)": "wattpv2",
        "ac current (a)": "ampac",
        "device working condition": "status",
    }
)

#sometimes theres a . at the end of updatetime, remove it
df2["updatetime"] = df2['updatetime'].str.strip('.')

# convert our timestamp to a datetime
df2["updatetime"] = pd.to_datetime(df2["updatetime"])

# make our new data time the index
df2.set_index("updatetime", inplace=True)

# append it to our DB
df2[
    [
        "amppv1",
        "voltpv1",
        "wattpv1",
        "amppv2",
        "voltpv2",
        "wattpv2",
        "ampac",
        "voltac",
        "wattac",
        "dayyeild",
        "totalyield",
        "status",
    ]
].to_sql("solar_generation", engine, if_exists="append")

# print the date of the first/last entry in this file
print("start: " + str(df2.index[0].date()))
print("end: " + str(df2.index[-1].date()))

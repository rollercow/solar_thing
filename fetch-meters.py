from datetime import datetime
from octopus_energy_api import oe_api
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://@/chris")

api_key = "api_key_goes_here"
account_number = "account_number_goes_here"
energy_api = oe_api(account_number, api_key)

b = energy_api.properties[0]["meters"][1]
foo = b.m[1]
start = datetime.fromisoformat(foo.start)
end = datetime.fromisoformat(foo.end)
bar = foo.consumption(start, end)
bar["interval_start"] = pd.to_datetime(bar["interval_start"], utc=True)
bar["interval_end"] = pd.to_datetime(bar["interval_end"], utc=True)
bar.to_sql("incoming_meter", engine, if_exists="append", index=False)

b = energy_api.properties[0]["meters"][0]
foo = b.m[0]
start = datetime.fromisoformat(foo.start)
end = datetime.fromisoformat(foo.end)
bar = foo.consumption(start, end)
bar["interval_start"] = pd.to_datetime(bar["interval_start"], utc=True)
bar["interval_end"] = pd.to_datetime(bar["interval_end"], utc=True)
bar.to_sql("outgoing_meter", engine, if_exists="append", index=False)

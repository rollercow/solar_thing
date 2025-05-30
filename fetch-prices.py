from octopus_energy_api import oe_api, tariff
from sqlalchemy import create_engine
import pandas as pd

api_key = "api_key_goes_here"
account_number = "account_number_goes_here"
energy_api = oe_api(account_number, api_key)
engine = create_engine("postgresql://@/chris")

con = []
b = energy_api.properties[0]["meters"][0]
for tar in b.agreements:
    bob = tariff.tarrif(
        energy_api, tar["tariff_code"], tar["valid_from"], tar["valid_to"]
    )
    con.append(bob.lookup())

barPrice = pd.concat(con)
barPrice.to_sql("outgoing_price", engine, if_exists="append", index=False)

con = []
b = energy_api.properties[0]["meters"][1]
for tar in b.agreements:
    bob = tariff.tarrif(
        energy_api, tar["tariff_code"], tar["valid_from"], tar["valid_to"]
    )
    con.append(bob.lookup())

barPrice = pd.concat(con)
barPrice.to_sql("incoming_price", engine, if_exists="append", index=False)

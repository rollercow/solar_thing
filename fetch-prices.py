from octopus_energy_api import oe_api, tariff
from sqlalchemy import create_engine

api_key = "api_key_goes_here"
account_number = "account_number_goes_here"
energy_api = oe_api(account_number, api_key)
engine = create_engine("postgresql://@/chris")

b = energy_api.properties[0]["meters"][0]
tar = b.agreements[0]
bob = tariff.tarrif(energy_api, tar["tariff_code"], tar["valid_from"], tar["valid_to"])
barPrice = bob.lookup()
barPrice.to_sql("outgoing_price", engine, if_exists="append", index=False)

b = energy_api.properties[0]["meters"][1]
tar = b.agreements[3]
bob = tariff.tarrif(energy_api, tar["tariff_code"], tar["valid_from"], tar["valid_to"])
barPrice = bob.lookup()
barPrice.to_sql("incoming_price", engine, if_exists="append", index=False)

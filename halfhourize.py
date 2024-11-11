from datetime import timedelta
import pandas as pd
from sqlalchemy import create_engine

# my Solax inverter seems to over estimate its lifetime power output by about
#  5% compared to the meter, this allows us to adjust for that later
solaxTotalGen = 10325.9
meterTotalGen = 9851.5
totalGenScale = meterTotalGen / solaxTotalGen

# connect to our DB
engine = create_engine("postgresql://@/chris")

# Pull back the imported excel data from the table we aggregate it in
df = pd.read_sql(
    "select distinct updatetime, wattac, dayyeild from solar_generation",
    engine,
    index_col="updatetime",
).sort_index()


def makeHalfHour(DaysData):
    """Builds nicely interpolated half hour windows for solar generation in kW/h
    from the 5min data the SolaX inverter reporting gives you"""
    # append a zero read to the end of the day, 5min after the end of our data,
    # since the inverter has gone to sleep now
    nextRowTimestamp = DaysData.index[-1] + timedelta(minutes=5)
    # make ourselves a new frame to append to the end of our data
    newFrame = pd.DataFrame(columns=["wattac"])
    newFrame.loc[nextRowTimestamp] = [0]
    # append it to the end
    newDaysData = pd.concat([DaysData, newFrame])
    # get a timestamp for the day
    thisDay = DaysData.index.to_period("D")[0].to_timestamp()
    # build a new index with an entry per min that we can add
    oneMinRangeIndex = pd.date_range(thisDay, periods=1440, freq="1T")
    oneMinFrame = pd.concat([newDaysData, pd.DatetimeIndex.to_frame(oneMinRangeIndex)])
    # interpolate to improve the resampleing to a 30min timebase
    # devide by two so we end up with a value in kWh
    return (
        oneMinFrame.sort_index()["wattac"]
        .interpolate(method="pchip", limit_area="inside")
        .resample("30T")
        .mean()
        / 2
    )


# create a list for our results
halfHourGen = []
# give me a day delta
aDay = timedelta(days=1)
# find the unique days in our blob of data
for day in df.index.to_period("D").unique():
    # make a timestamp
    thisDay = day.to_timestamp()
    # use it to slice our data blob
    daySlice = df.loc[thisDay : thisDay + aDay]  # noqa: E203
    # generate our half hourly return
    meterLikeData = makeHalfHour(daySlice)
    realYeild = daySlice["dayyeild"].max()
    estYeild = meterLikeData.sum()
    # work out the ratio between calculated and real yeild
    # scaled to adjust for total generation according to the meter rather
    # than the inverter
    dailyYeildRatio = ((realYeild * 1000) * totalGenScale) / estYeild
    # print our ratio
    # print(str(day) + " - " + str(dailyYeildRatio))
    # scale our days data based on the ratio
    scaledMeterLikeData = meterLikeData * dailyYeildRatio
    # feed that into the list to build a results frame
    halfHourGen.append(scaledMeterLikeData.dropna())

solarMeterEquiv = pd.concat(halfHourGen)
# write it out to the DB
solarMeterEquiv.to_sql("solar_meter", engine, if_exists="append")

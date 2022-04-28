from datetime import timedelta
import pandas as pd

df2 = pd.read_excel("foo.xls", skiprows=4)

# find the unique days in our blob of data
df2.index.to_period("D").unique()

# append a zero to the end of the day
next = df2.index[-1] + timedelta(minutes=5)
df = pd.DataFrame(columns=["wattac"])
df.loc[next] = [0]
pd.concat([df2, df])

# interpolate to improve the resampleing
foo = pd.date_range("2022-02-24", periods=1440, freq="1T")
bar = pd.concat([df2, pd.DatetimeIndex.to_frame(foo)])
bar.sort_index()["wattac"].interpolate(method="pchip", limit_area="inside").resample(
    "1h"
).mean()


def makeHalfHour(DaysData):
    # append a zero to the end of the day, 5min after the end of our data
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
for day in df2.index.to_period("D").unique():
    # make a timestamp
    thisDay = day.to_timestamp()
    # use it to slice our data blob and generate our half hourly return
    halfHourGen.append(makeHalfHour(df2.loc[thisDay : thisDay + aDay]))  # noqa: E203
solarMeterEquiv = pd.concat(halfHourGen)

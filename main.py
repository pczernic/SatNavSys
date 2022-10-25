import pandas as pd
import functions
from classes import Satellite
from visualization import viewer

pd.set_option('display.max_rows', None)

# almanac_path = r"http://celestrak.org/GPS/almanac/Yuma/2022/almanac.yuma.week0182.405504.txt"
almanac_path = r'almanac.yuma.week0182.405504.txt'
almanac_data = pd.read_csv(almanac_path, delimiter=':', names=['name', 'value'])
# print(almanac_data)

sat_index_df = almanac_data[almanac_data['value'].isna()]
sat_index = sat_index_df.index.tolist()

sats = []
for i in sat_index:
    sats.append(Satellite(almanac_data.iat[i + 1, 1], almanac_data.iat[i + 2, 1], almanac_data.iat[i + 3, 1],
                          almanac_data.iat[i + 4, 1], almanac_data.iat[i + 5, 1], almanac_data.iat[i + 6, 1],
                          almanac_data.iat[i + 7, 1], almanac_data.iat[i + 8, 1], almanac_data.iat[i + 9, 1],
                          almanac_data.iat[i + 10, 1], almanac_data.iat[i + 11, 1], almanac_data.iat[i + 12, 1],
                          almanac_data.iat[i + 13, 1]))

week, tow = functions.date2gpstime([2022, 10, 11, 12, 0, 0])

# task 1 - calculate xyz coordinates for all satellites in one epoch
sat_positions = []
for sat in sats:
    sat_positions.append(sat.calculate_position(tow, week))


# task 2 - calculate for the whole day for each sat (interval 15 min)
sats_daily_positions = []

week2, tow2 = functions.date2gpstime([2022, 10, 11, 0, 0, 0])

interval = []

for i in range(0, 24 * 60 * 60, 15 * 60):
    interval.append(i)

for i in interval:
    tow2 += i
    for sat in sats:
        sats_daily_positions.append(sat.calculate_position(tow2, week2))

daily_df = pd.DataFrame(sats_daily_positions, columns=['sat_id', 'tow', 'X', 'Y', 'Z'])
daily_df.sort_values(by=['tow'])
daily_df.plot()
print(daily_df)

viewer(daily_df)

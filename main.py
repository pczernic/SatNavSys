import urllib.request
import pandas as pd

pd.set_option('display.max_rows', None)

almanac_path = r"http://celestrak.org/GPS/almanac/Yuma/2022/almanac.yuma.week0182.405504.txt"

almanac = urllib.request.urlopen(almanac_path)
almanac_data = pd.read_csv(almanac_path)

#
# df = pd.DataFrame(almanac_data)
# print(df.loc[[0]])

import pandas as pd
import numpy as np


class Satellite:
    def __init__(self, sat_id, health, eccentricity, time_of_applicability, orbital_inclination, rate_of_right_ascen,
                 sqrt, right_ascen_at_week, argument_of_perigee, mean_anom, af0, af1, week):
        self.n = None
        self.tk = None
        self.a = None
        self.time = None
        self.condition = None
        self.week = week
        self.af1 = af1
        self.af0 = af0
        self.mean_anom = mean_anom
        self.argument_of_perigee = argument_of_perigee
        self.right_ascen_at_week = right_ascen_at_week
        self.sqrt = sqrt
        self.rate_of_right_ascen = rate_of_right_ascen
        self.orbital_inclination = orbital_inclination
        self.time_of_applicability = time_of_applicability
        self.health = health
        self.id = int(sat_id)
        self.e = eccentricity


    def print_info(self):
        if self.health == 0:
            self.condition = 'OK'
        else:
            self.condition = 'NOT OK!!!'
        print(f'========================\n'
              f'Satellite {self.id}\n'
              f'Health condition: {self.condition}\n'
              f'========================')

    def calculate_position(self, time):
        self.time = time

        self.tk = self.time - self.time_of_applicability
        self.a = self.sqrt ** 2
        self.n = np.sqrt((MU / self.a ** 3))
        self.mk = self.mean_anom + self.n * self.tk

        self.ek1 = self.mk
        self.ek2 = self.mk + self.e * np.sin(self.ek1)
        self.diff = np.abs(self.ek1 - self.ek2)
        while self.diff > 10e-12:
            pass
        # print(self.ek)
        # while self.ek


###########################################################################################
MU = 3.986004115e14
OMEGA_E = 7.2921151467e-5


pd.set_option('display.max_rows', None)

almanac_path = r"http://celestrak.org/GPS/almanac/Yuma/2022/almanac.yuma.week0182.405504.txt"
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

print(sats[0].e)
# print(sats[26].calculate_position(12534657))


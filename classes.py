import numpy as np

MU = 3.986005e14
OMEGA_E = 7.2921151467e-5


class Satellite:
    def __init__(self, sat_id, health, eccentricity, time_of_applicability, orbital_inclination, rate_of_right_ascen,
                 sqrt, right_ascen_at_week, argument_of_perigee, mean_anom, af0, af1, gps_week):
        self.vk = None
        self.e_previous = None
        self.e_next = None
        self.i = None
        self.diff = None
        self.ek2 = None
        self.ek1 = None
        self.mk = None
        self.n = None
        self.tk = None
        self.a = None
        self.time = None
        self.condition = None
        self.gps_week = gps_week
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

    def calculate_position(self, tow, week):
        self.tow = tow
        self.week = week
        # step 1
        self.tk = (self.tow + self.week * 7 * 86400) - (self.time_of_applicability + self.gps_week * 7 * 86400)
        # print(f'tk = {self.tk}')
        # step 2
        self.a = self.sqrt ** 2
        # print(f'a = {self.a}')
        # step 3
        self.n = np.sqrt((MU / self.a ** 3))
        # print(f'n = {self.n}')
        # step 4
        self.mk = self.mean_anom + self.n * self.tk
        # print(self.mk)
        # step 5
        self.e_previous = self.mk
        self.i = 1
        while True:
            self.e_next = self.mk + self.e * np.sin(self.e_previous)
            # print(f'    iteration {self.i} = {self.e_next}')
            self.i += 1
            if np.abs(self.e_previous - self.e_next) < 10e-12:
                break
                print('Done')
            self.e_previous = self.e_next
        # step 6
        self.vk = np.arctan2((np.sqrt(1 - self.e ** 2) * np.sin(self.e_next)), (np.cos(self.e_next) - self.e))
        print(self.vk)

        # step 7
        self.fi = self.vk + self.argument_of_perigee

        # step 8
        # self.rk = self.a *
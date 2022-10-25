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
        print(f'====================\n'
              f'Satellite {self.id}\n'
              f'Health condition: {self.condition}\n'
              f'====================')

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
        # print(f'Mk = {self.mk}')

        # step 5
        self.e_previous = self.mk % (2 * np.pi)
        # print(f'Ek = {self.e_previous}')
        self.i = 1
        while True:
            self.e_next = self.mk + self.e * np.sin(self.e_previous)
            # print(f'    iteration {self.i} = {self.e_next % (2 * np.pi)}')
            self.i += 1
            if np.abs(self.e_previous - self.e_next) < 10e-12:
                # print('Done')
                break
            self.e_previous = self.e_next

        # step 6
        self.vk = np.arctan2((np.sqrt(1 - self.e ** 2) * np.sin(self.e_next)), (np.cos(self.e_next) - self.e))
        # print(f'vk = {self.vk}')

        # step 7
        self.uk = self.vk + self.argument_of_perigee
        # print(f'uk = {self.uk}')

        # step 8
        self.rk = self.a * (1 - self.e * np.cos(self.e_next))
        # print(f'rk = {self.rk}')

        # step 9
        self.xk = self.rk * np.cos(self.uk)
        self.yk = self.rk * np.sin(self.uk)
        # print(f'xk = {self.xk}\nyk = {self.yk}')

        # step 10
        self.omega_k = self.right_ascen_at_week + (self.rate_of_right_ascen - OMEGA_E) * self.tk - OMEGA_E * self.time_of_applicability
        # print(f'omega_k = {self.omega_k}')

        # step 11
        self.x = self.xk * np.cos(self.omega_k) - self.yk * np.cos(self.orbital_inclination) * np.sin(self.omega_k)
        self.y = self.xk * np.sin(self.omega_k) + self.yk * np.cos(self.orbital_inclination) * np.cos(self.omega_k)
        self.z = self.yk * np.sin(self.orbital_inclination)
        print(f'====================\n'
              f'Position of Satelite {self.id}:\nXk = {self.x}\nYk = {self.y}\nZk = {self.z}\n'
              f'====================')
        return [self.x, self.y, self.z]

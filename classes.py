class Satellite:
    def __init__(self, sat_id, health, time_of_applicability, orbital_inclination, rate_of_right_ascen, sqrt,
                 right_ascen_at_week, argument_of_perigee, mean_anom, af0, af1, week):
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

    def print_info(self):
        if self.health == 0:
            self.condition = 'OK'
        else:
            self.condition = 'NOT OK!!!'
        print(f'========================\n'
              f'Satellite {self.id}\n'
              f'Health condition: {self.condition}\n'
              f'========================')

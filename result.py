class Result:
    def __init__(self, population=None, seats=None, seats_before_rounding=None):
        self.population = population
        self.seats = seats
        self.seats_before_rounding = seats_before_rounding

    @property
    def population_per_seat(self):
        return self.population / self.seats

    @property
    def population_per_seat_before_rounding(self):
        return self.population / self.seats_before_rounding

    def __str__(self):
        return "pop: {}, seats: {} ({}), pop/seat: {} ({})".format(self.population, self.seats,
                                                                   self.seats_before_rounding,
                                                                   self.population_per_seat,
                                                                   self.population_per_seat_before_rounding)

    def __repr__(self):
        return str(self)

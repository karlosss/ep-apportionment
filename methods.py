from copy import deepcopy
from math import ceil, floor

from population import get_pop
from result import Result
from sorting import by_value


def real(year):
    if year != 2013:
        raise RuntimeError("Impossible")
    pop = get_pop(year)
    tmp = deepcopy(pop)
    tmp["Belgium"] = Result(pop["Belgium"], 21, 21)
    tmp["Bulgaria"] = Result(pop["Bulgaria"], 17, 17)
    tmp["Czechia"] = Result(pop["Czechia"], 21, 21)
    tmp["Denmark"] = Result(pop["Denmark"], 13, 13)
    tmp["Germany"] = Result(pop["Germany"], 96, 96)
    tmp["Estonia"] = Result(pop["Estonia"], 6, 6)
    tmp["Ireland"] = Result(pop["Ireland"], 11, 11)
    tmp["Greece"] = Result(pop["Greece"], 21, 21)
    tmp["Spain"] = Result(pop["Spain"], 54, 54)
    tmp["France"] = Result(pop["France"], 74, 74)
    tmp["Croatia"] = Result(pop["Croatia"], 11, 11)
    tmp["Italy"] = Result(pop["Italy"], 73, 73)
    tmp["Cyprus"] = Result(pop["Cyprus"], 6, 6)
    tmp["Latvia"] = Result(pop["Latvia"], 8, 8)
    tmp["Lithuania"] = Result(pop["Lithuania"], 11, 11)
    tmp["Luxembourg"] = Result(pop["Luxembourg"], 6, 6)
    tmp["Hungary"] = Result(pop["Hungary"], 21, 21)
    tmp["Malta"] = Result(pop["Malta"], 6, 6)
    tmp["Netherlands"] = Result(pop["Netherlands"], 26, 26)
    tmp["Austria"] = Result(pop["Austria"], 18, 18)
    tmp["Poland"] = Result(pop["Poland"], 51, 51)
    tmp["Portugal"] = Result(pop["Portugal"], 21, 21)
    tmp["Romania"] = Result(pop["Romania"], 32, 32)
    tmp["Slovenia"] = Result(pop["Slovenia"], 8, 8)
    tmp["Slovakia"] = Result(pop["Slovakia"], 13, 13)
    tmp["Finland"] = Result(pop["Finland"], 13, 13)
    tmp["Sweden"] = Result(pop["Sweden"], 20, 20)
    tmp["United Kingdom"] = Result(pop["United Kingdom"], 73, 73)
    return tmp


def base_prop(year, b=5, parliament_size=751, max_seats=96, round=ceil):
    pop = get_pop(year)
    tmp = deepcopy(pop)

    rem = 0
    for item in tmp:
        rem += b
        tmp[item] = Result(pop[item])

    rem = parliament_size - rem

    d = sum(pop.values())/rem

    x = None
    while True:
        for item in pop:
            tmp[item].seats = min(round(pop[item]/d), max_seats-b)
            tmp[item].seats_before_rounding = min(pop[item]/d, max_seats-b)

        seats = [x.seats for x in tmp.values()]

        if sum(seats) == rem:
            print(d)
            break
        elif sum(seats) > rem:
            d += d*0.00001
            if x is False:
                raise RuntimeError("Impossible")
            x = True
        else:
            d -= d * 0.00001
            if x is True:
                raise RuntimeError("Impossible")
            x = False

    for item in tmp:
        tmp[item].seats += b
        tmp[item].seats_before_rounding += b

    return tmp


def spline(year, min_seats=6, parliament_size=751, max_seats=96, round=ceil):
    pop = get_pop(year)
    tmp = deepcopy(pop)

    for item in tmp:
        tmp[item] = Result(pop[item])

    d = sum(pop.values()) / parliament_size
    min_pop = min(pop.values())

    x = None
    while True:
        for item in pop:
            tmp[item].seats_before_rounding = min(min_seats + (pop[item]-min_pop) / d, max_seats)
            tmp[item].seats = round(tmp[item].seats_before_rounding)

        seats = [x.seats for x in tmp.values()]

        if sum(seats) == parliament_size:
            break
        elif sum(seats) > parliament_size:
            d += d * 0.00001
            if x is False:
                raise RuntimeError("Impossible")
            x = True
        else:
            d -= d * 0.00001
            if x is True:
                raise RuntimeError("Impossible")
            x = False

    return tmp


def hamilton(year, min_seats=6, parliament_size=751, max_seats=96):
    pop = get_pop(year)
    tmp = deepcopy(pop)

    for item in tmp:
        tmp[item] = Result(pop[item])

    total_pop = sum([pop[x] for x in pop])

    rem = parliament_size

    for item in tmp:
        tmp[item].seats_before_rounding = (tmp[item].population/total_pop)*parliament_size
        tmp[item].seats = floor(tmp[item].seats_before_rounding)
        tmp[item].seats = min(tmp[item].seats, max_seats)
        tmp[item].seats = max(tmp[item].seats, min_seats)
        rem -= tmp[item].seats

    srt = by_value(tmp, lambda x: -(x[1].seats_before_rounding-x[1].seats))
    order = list(srt.keys())
    i = 0
    while rem > 0:
        if tmp[order[i]].seats < max_seats:
            tmp[order[i]].seats += 1
            rem -= 1
        i = (i + 1) % len(tmp)

    return tmp


def dhondt(year, min_seats=6, parliament_size=751, max_seats=96):
    pop = get_pop(year)
    tmp = deepcopy(pop)

    rem = parliament_size
    for item in tmp:
        rem -= min_seats
        tmp[item] = Result(pop[item])
        tmp[item].seats = min_seats
        tmp[item].seats_before_rounding = min_seats
        tmp[item].tmppop = tmp[item].population
        tmp[item].tmpdiv = 1

    ks = list(tmp.keys())
    while rem > 0:
        ks.sort(key=lambda x: -tmp[x].tmppop)
        i = 0
        while tmp[ks[i]].seats == max_seats:
            i += 1
        tmp[ks[i]].seats += 1
        tmp[ks[i]].seats_before_rounding += 1
        tmp[ks[i]].tmpdiv += 1
        tmp[ks[i]].tmppop = tmp[ks[i]].population/tmp[ks[i]].tmpdiv
        rem -= 1

    return tmp
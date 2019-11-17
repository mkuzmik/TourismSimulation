import logging
from datetime import datetime
from operator import itemgetter
from time import strptime

import numpy as np

log = logging.getLogger('SchedulesGenerator')


class SchedulesGenerator:

    def __init__(self, pois, debug):
        self.pois = pois
        self.debug = debug

    def _time_from_timestamp(self, timestamp):
        tmp = datetime.fromtimestamp(timestamp)
        return (tmp.hour * 60) + tmp.minute

    def _time_from_string(self, time_string):
        tmp = strptime(time_string, '%H:%M')
        return (tmp.tm_hour * 60) + tmp.tm_min

    def generate(self, agent, timestamp):
        """Schedule generator
            1. Rand time to spend in the city with poisson distribution,
                agent wants to end trip after this time (and start returning to initial spawn point)
            2. Sort pois by (approximation of) distance, assign "points" to them in range <1,3> (linear function)
            3. Multiply "points" by attractiveness
            4. Divide by difference between agent's wealth and poi price
            5. Add or substract "points" based on agent's age, domestic, education, intoxication and poi type
            6. Get as much as agent is able to rich in his time, taking only pois that will be open
        """
        time_to_spend = np.random.poisson(4) * 3600  # in seconds
        log.debug("Scheduling start\nTime to spend: {}h".format(time_to_spend / 3600))
        log.debug("Agent:")
        log.debug("    age: {}".format(agent.age))
        log.debug("    wealth: {}".format(agent.wealth))
        log.debug("    domestic: {}".format(agent.domestic))
        log.debug("    education: {}".format(agent.education))
        log.debug("    intoxication: {}".format(agent.intoxication))
        log.debug("    speed: {}".format(agent.speed))
        log.debug("")

        pois_with_distances = sorted(
            [(poi, (agent.posx - poi.x) ** 2 + (agent.posy - poi.y) ** 2) for poi in self.pois],
            key=itemgetter(1))
        log.debug("Distances:")
        log.debug([poi.name + " - " + str(distance) for poi, distance in pois_with_distances])
        log.debug("")

        x1, x2 = pois_with_distances[0][1], pois_with_distances[-1][1]
        linear_func_a, linear_func_b = 2. / (x1 - x2), 1 - ((2. * x2) / (x1 - x2))

        pois_with_points = map(lambda pwd: (pwd[0], linear_func_a * pwd[1] + linear_func_b), pois_with_distances)
        pois_with_points = list(pois_with_points)
        log.debug("After distance points:")
        log.debug([poi.name + " - " + str(points) for poi, points in
                   sorted(pois_with_points, key=itemgetter(1), reverse=True)])
        log.debug("")

        pois_with_points = map(lambda pwd: (pwd[0], pwd[1] * pwd[0].attractiveness), pois_with_points)
        pois_with_points = list(pois_with_points)
        log.debug("After attractiveness points:")
        log.debug([poi.name + " - " + str(points) for poi, points in
                   sorted(pois_with_points, key=itemgetter(1), reverse=True)])
        log.debug("")

        pois_with_points = list(
            map(lambda pwd: [pwd[0], pwd[1] / (1 + abs(agent.wealth - pwd[0].price))], pois_with_points))
        log.debug("After wealth-price points:")
        log.debug([poi.name + " - " + str(points) for poi, points in
                   sorted(pois_with_points, key=itemgetter(1), reverse=True)])
        log.debug("")

        # poi points should be in range <10/11 - 30>
        # poi_types = ["Heritage", "Other", "Club", "Museum", "Restaurant"]
        for i in range(len(pois_with_points)):
            if agent.intoxication > 8 and pois_with_points[i][0].type == "Club":
                pois_with_points[i][1] *= 5
            elif agent.intoxication > 5 and pois_with_points[i][0].type == "Club":
                pois_with_points[i][1] *= 2

            if agent.education > 8 and pois_with_points[i][0].type in ("Heritage", "Museum"):
                pois_with_points[i][1] *= 1.5
            elif agent.education > 5 and pois_with_points[i][0].type in ("Heritage", "Museum"):
                pois_with_points[i][1] *= 1.2

            if agent.domestic == 1 and pois_with_points[i][0].type == "Heritage":
                pois_with_points[i][1] *= 1.2
        log.debug("After custom modifications points:")
        log.debug([poi.name + " - " + str(points) for poi, points in
                   sorted(pois_with_points, key=itemgetter(1), reverse=True)])
        log.debug("")

        pois_sorted_with_points = sorted(pois_with_points, key=itemgetter(1), reverse=True)

        log.debug("Get as much pois as can:")
        schedule = []
        time_approximation = 0
        for poi, points in pois_sorted_with_points:
            distance = np.sqrt((agent.posx - poi.x) ** 2 + (agent.posy - poi.y) ** 2)
            time_approximation_tmp = time_approximation + (distance / agent.speed)

            log.debug("Poi {} ({}): distance = {}  | arrival_time = {}".format(poi.name, points, distance,
                                                                               time_approximation_tmp))
            log.debug("Time arrival: {} {}".format(self._time_from_timestamp(timestamp + time_approximation_tmp),
                      datetime.fromtimestamp(timestamp + time_approximation_tmp).strftime('%Y-%m-%d %H:%M:%S')))
            log.debug("Time open: {} {}".format(self._time_from_string(poi.time_open),
                      datetime.fromtimestamp(self._time_from_string(poi.time_open)).strftime('%Y-%m-%d %H:%M:%S')))
            log.debug("Time leave: {} {}".format(
                      self._time_from_timestamp(timestamp + time_approximation_tmp + (poi.time_needed * 60)),
                      datetime.fromtimestamp(timestamp + time_approximation_tmp + (poi.time_needed * 60)).strftime(
                          '%Y-%m-%d %H:%M:%S')))
            log.debug("Time close: {} {}".format(self._time_from_string(poi.time_close),
                      datetime.fromtimestamp(self._time_from_string(poi.time_close)).strftime('%Y-%m-%d %H:%M:%S')))
            log.debug("")
            # check if agent will be there after open and before close
            if self._time_from_timestamp(timestamp + time_approximation_tmp) >= self._time_from_string(
                    poi.time_open) and \
                    self._time_from_timestamp(
                        timestamp + time_approximation_tmp + (poi.time_needed * 60)) <= self._time_from_string(
                poi.time_close):
                schedule.append(poi)
                time_approximation += (distance / agent.speed) + (poi.time_needed * 60)

            if time_approximation >= time_to_spend:
                break

        if len(schedule) == 0:
            schedule.append(pois_sorted_with_points[0][0])

        schedule.reverse()  # we will pop from the end
        log.debug("Final schedule:")
        log.debug([poi.name for poi in schedule])

        return schedule

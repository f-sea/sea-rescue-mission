'''----------------------------------------------------------------------------------------------
Needed Python libraries and modules
-------------------------------------------------------------------------------------------------'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import ion, show
import os
'''----------------------------------------------------------------------------------------------
Define required classes
-------------------------------------------------------------------------------------------------'''


class ships:
    def __init__(self, myid, vel, cap, x_pos, y_pos, no):
        self.id = myid
        self.vel = vel
        self.cap = cap
        self.x = x_pos
        self.y = y_pos
        self.no_total = no
        self.no_on_port = no
        self.score = 0
        self.distance_covered = 0
        self.save_time = 0
        self.critical_time = 0
        self.cap_left = cap

    def getefficiency(self):
        """Each ship's capability is measured as the product of its capacity and its velocity"""
        self.score = self.cap * self.vel
        eff = self.score
        return eff

    def determine_costs(self, points):
        costs = np.array([])
        for point in points:
            distance = np.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
            people_to_save = point.closeby
            cost = distance / people_to_save
            costs = np.append(costs, cost)
        return costs

    def minimize_cost(self, costs):
        min_pos = np.argmin(costs)
        return min_pos

    def are_available(self):
        if (self.no_on_port > 0):
            flag = 'available'
        else:
            flag = 'occupied'
        return flag

    def time_to_save(self):
        self.save_time = self.distance_covered / self.vel

    def critical_time_log(self):
        if ((self.critical_time == 0) or (self.save_time <= self.critical_time)):
            self.critical_time = self.save_time
        else:
            pass


class people_in_danger:  # Info by special tranceiver embedded in life jacket
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.closeby = 0
        self.id = 'solitary'
        self.cost = np.Infinity
        self.path = None
        self.visited = False

    def determine_clusters(self, other_people):
        occurencies = other_people.count(self)
        for person in other_people:
            if (((person.x - self.x)**2 + (person.y - self.y)**2) <= 4.5**2):
                self.closeby = self.closeby + 1
                if (occurencies == 1):
                    pass
                else:
                    other_people.remove(person)
        return other_people

    def determine_cost(self, path_current_cost, sp):
        print('Point1: \t', sp.x, sp.y)
        print('Point2: \t', self.x, self.y)
        distance = np.sqrt((self.x - sp.x)**2 + (self.y - sp.y)**2)
        cost = path_current_cost + self.closeby / distance
        self.cost = np.minimum(cost, self.cost)
        if (self.cost == cost):
            self.path = sp


class circle:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy


class coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class bcolors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


'''----------------------------------------------------------------------------------------------
Function's toolbox
-------------------------------------------------------------------------------------------------'''

# Ship fleet setting and ranking


def getfleet(port_x, port_y):
    all_ships = []
    # Rescue fleet available by port (is set to be random in each run)
    print(bcolors.UNDERLINE + "Case study's total ship fleet \n" + bcolors.ENDC)
    ship1 = ships('Maya 850', vel_kn_to_ms(25), 17, port_x, port_y, np.random.randint(1, 10))  # Maya 850 by Norsafe
    ship2 = ships('Matrix 450', vel_kn_to_ms(6), 6, port_x, port_y, np.random.randint(1, 10))  # Matrix 450 by Norsafe
    ship3 = ships('FRC 1204', vel_kn_to_ms(35), 56, port_x, port_y, np.random.randint(1, 10))  # frc 1204 by fastrescuecraft.nl
    for ship in [ship1, ship2, ship3]:
        print(ship.id, ": \t", ship.no_total, '\n')
        all_ships.append(ship)
    return all_ships


def organise_ships_by_job_efficiency(all_ships):
    all_eff = []
    for ship in all_ships:
        capab = ship.getefficiency()
        all_eff.append(capab)
    all_eff = np.asarray(all_eff)
    ind_sorted = np.argsort(all_eff)
    return ind_sorted
#-------------------------------------------------------------------------------------------------------------------------------


def process_points(points):
    for point in points:
        points = point.determine_clusters(points)
    for point in points:
        if (point.closeby > 1):
            point.id = 'cluster'  # Points categorization as clusters and solitaries
    return points


#--------------------------------------------------------------------------------------------------------------------------------

# Finds the shortest route by saving as many people as possible in as little time as possible


def dijskra_algorithm(people_in_danger, all_ships, port_x, port_y, show_animation, human_endurance_water_seconds, cluster_labels, cl_pos):
    '''
    ship_ranking = organise_ships_by_job_efficiency(all_ships)
    saved_points = []
    points_to_visit = people_in_danger
    paths = []
    colors = ["m", "g", "y"]
    sh_path = shortest_path(port_x, port_y, points_to_visit)
    for rk in reversed(ship_ranking):
        plt.pause(0.0001)
        ship = all_ships[rk]
        color = colors[rk]
        for jj in range(0, ship.no_total):
            print(bcolors.BOLD + "Ship \t", ship.id, "(", jj + 1, "/", ship.no_total, ") \t takes over the mission" + bcolors.ENDC)
            ship.no_on_port = ship.no_on_port - 1
            whole_cap = ship.cap
            start_xpos = ship.x
            start_ypos = ship.y
            people_no_boarded = 0
            ship_path = []
            for point in sh_path:
                try:
                    people_no_boarded = people_no_boarded + point.closeby
                except:
                    pass
                if (people_no_boarded <= ship.cap_left):
                    ship_path.append(point)
                    sh_path.remove(point)
                    try:
                        ship.cap_left = ship.cap_left - point.closeby
                    except:
                        pass
                else:
                    break
            paths.append(ship_path)
            for point in ship_path:
                saved_points.append(point)
                try:
                    points_to_visit.remove(point)
                except:
                    pass
            ii = 0
            for point in reversed(ship_path):
                plt.show()
                if (ii == 0):
                    predecessor = ship_path[-1]
                    ii = ii + 1
                else:
                    plt.plot([predecessor.x, point.x], [predecessor.y, point.y], color + "-")
                    predecessor = point
                    plt.pause(0.1)
           # print(bcolors.CYAN + "People left behind: \t" + bcolors.ENDC, bcolors.WARNING + "", sum, "" + bcolors.ENDC, bcolors.CYAN + "\t Ship capacity left (persons):" + bcolors.ENDC, bcolors.WARNING + "", ship.cap, "" + bcolors.ENDC)
            ship.cap = whole_cap
            ship.x = start_xpos
            ship.y = start_ypos
        plt.show()
    #mission_overview(all_ships, sum, saved_points)


def plot_paths():
    if show_animation:
        plt.show()
        plt.plot([ship.x, point_saved.x], [ship.y, point_saved.y], color + "-")
        plt.pause(0.0001)

 '''
    ship_ranking = organise_ships_by_job_efficiency(all_ships)
    port = coordinates(port_x, port_y)
    saved_points = []
    points_to_visit = people_in_danger
    colors = ["m", "g", "y"]
    for rk in reversed(ship_ranking):
        plt.pause(0.0001)
        ship = all_ships[rk]
        color = colors[rk]
        for jj in range(0, ship.no_total):
            if (os.name == 'posix'):
                print(bcolors.BOLD + "Ship \t", ship.id, "(", jj + 1, "/", ship.no_total, ") \t takes over the mission" + bcolors.ENDC)
            else:
                print("Ship \t", ship.id, "(", jj + 1, "/", ship.no_total, ") \t takes over the mission")
            ship.no_on_port = ship.no_on_port - 1
            whole_cap = ship.cap
            start_xpos = ship.x
            start_ypos = ship.y
            startpoint = coordinates(start_xpos, start_ypos)
            surpassed_critical_point = False
            current = []
            predecessors = []
            while (ship.cap > 0):
                if (len(points_to_visit) == 0):
                    break
                weights = ship.determine_costs(points_to_visit)
                destination = ship.minimize_cost(weights)
                point_saved = points_to_visit[destination]
                current.append(point_saved)
                predecessors.append(startpoint)
                ship.distance_covered = ship.distance_covered + np.sqrt((start_xpos - point_saved.x)**2 + (start_ypos - point_saved.y)**2)
                if (point_saved.closeby > ship.cap):
                    index = cl_pos.index([point_saved.x, point_saved.y])
                    print(index)
                    point_saved.closeby = point_saved.closeby - ship.cap
                    cluster_labels[index].s = point_saved.closeby
                    cluster_labels[index].color = 'magenda'
                    break
                else:
                    points_to_visit.remove(point_saved)
                    saved_points.append(point_saved)
                    ship.cap = ship.cap - point_saved.closeby
                ship.time_to_save()
                if ((ship.save_time >= human_endurance_water_seconds) and (surpassed_critical_point == False)):
                    surpassed_critical_point = True
                    ship.critical_time_log()
                if show_animation:
                    plt.show()
                    plt.plot([ship.x, point_saved.x], [ship.y, point_saved.y], color + "-")
                    plt.pause(0.0001)
                ship.x = point_saved.x
                ship.y = point_saved.y
                sum = 0
            for point in points_to_visit:
                sum = sum + point.closeby
            if (os.name == 'posix'):
                print(bcolors.CYAN + "People left behind: \t" + bcolors.ENDC, bcolors.WARNING + "", sum, "" + bcolors.ENDC, bcolors.CYAN + "\t Ship capacity left (persons):" + bcolors.ENDC, bcolors.WARNING + "", ship.cap, "" + bcolors.ENDC)
            else:
                print("People left behind: \t", sum, "\t Ship capacity left (persons): \t", ship.cap)
            ship.cap = whole_cap
            ship.x = start_xpos
            ship.y = start_ypos
        plt.show()
    mission_overview(all_ships, sum, saved_points)
    return saved_points


# Finds the shortest route by saving as many people as possible in as little time as possible


def astar_algorithm(areas_centers, people_endangered, ship1, ship2, ship3, port_x, port_y):
    pass


def shortest_path(port_x, port_y, points_to_visit):
    start = coordinates(port_x, port_y)
    accumulated_cost = 0
    visited = []
    ii = 0
    while(points_to_visit):
        for point in points_to_visit:
            point.determine_cost(accumulated_cost, start)
        try:
            points_to_visit.remove(start)
        except:
            pass
        if (points_to_visit):
            destination = minimum_cost(points_to_visit)
            start = points_to_visit[destination]
            accumulated_cost = accumulated_cost + start.cost
        visited.append(start)
    visited.insert(0, coordinates(port_x, port_y))
    path = []
    last_point = visited[-1]
    while (len(path) != len(visited)):
        path.append(last_point)
        last_point = point.path
    return path


def minimum_cost(points):
    min_id = 0
    minimum_cost = np.Infinity
    for point in points:
        if (point.cost <= minimum_cost):
            minimum_cost = point.cost
            min_id = points.index(point)
    return min_id


def mission_time(ships):
    times = []
    crit_times = []
    for ship in ships:
        ship.time_to_save()
        times.append(ship.save_time)
        crit_times.append(ship.critical_time)
    return [min(crit_times), max(times)]


def mission_overview(ships, remaining, savedp):
    print("\n Mission Result")
    print("===============")
    saved = 0
    for point in savedp:
        saved = saved + point.closeby
    print("People saved:      \t", saved)
    print("People left behind: \t", remaining)
    [crit_time, time] = mission_time(ships)
    print("Established in [s]: \t", format(time, '.2f'))
    print("Critical time [s]: \t", format(crit_time, '.2f'))
    print("Proclaimed:         Successfull")
# This function converts velocity to SI units


def vel_kn_to_ms(vel):
    vel_ms = vel * 0.5144
    return vel_ms

# This is the program's main module and gets executed first

'''----------------------------------------------------------------------------------------------
Needed Python libraries and modules
-------------------------------------------------------------------------------------------------'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import ion, show
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

    def getefficiency(self):
        """Each ship's capability is measured as the product of its capacity and its velocity"""
        self.score = self.cap * self.vel
        eff = self.score
        return eff

    def determine_weights(self, points):
        weights = np.array([])
        for point in points:
            distance = np.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
            people_to_save = point.closeby
            weight = distance / people_to_save
            weights = np.append(weights, weight)
        return weights

    def minimize_cost(self, costs):
        min_pos = np.argmin(costs)
        return min_pos

    def are_available(self):
        if (self.no_on_port > 0):
            flag = 'available'
        else:
            flag = 'occupied'
        return flag

    def time_to_save(self, x):
        save_time = self.vel * x
        save_time_per_person = save_time / self.cap
        return save_time_per_person


class people_in_danger:  # Info by special tranceiver embedded in life jacket
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.closeby = 0
        self.id = 'solitary'

    def determine_clusters(self, other_people):
        for person in other_people:
            if (((person.x - self.x)**2 + (person.y - self.y)**2) <= 4.5**2):
                self.closeby = self.closeby + 1
                if ((person.x == self.x) and (person.y == self.y)):
                    pass
                else:
                    other_people.remove(person)
        return other_people


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


def dijskra_algorithm(people_in_danger, all_ships, port_x, port_y, show_animation):
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
            print(bcolors.BOLD + "Ship \t", ship.id, "(", jj + 1, "/", ship.no_total, ") \t takes over the mission" + bcolors.ENDC)
            ship.no_on_port = ship.no_on_port - 1
            whole_cap = ship.cap
            start_xpos = ship.x
            start_ypos = ship.y
            while (ship.cap > 0):
                if (len(points_to_visit) == 0):
                    break
                weights = ship.determine_weights(points_to_visit)
                destination = ship.minimize_cost(weights)
                point_saved = points_to_visit[destination]
                if (point_saved.closeby > ship.cap):
                    point_saved.closeby = point_saved.closeby - ship.cap
                    break
                else:
                    points_to_visit.remove(point_saved)
                    saved_points.append(point_saved)
                    ship.cap = ship.cap - point_saved.closeby
                if show_animation:
                    plt.show()
                    plt.plot([ship.x, point_saved.x], [ship.y, point_saved.y], color + "-")
                    plt.pause(0.0001)
                ship.x = point_saved.x
                ship.y = point_saved.y
                sum = 0
            for point in points_to_visit:
                sum = sum + point.closeby
            print(bcolors.CYAN + "People left behind: \t" + bcolors.ENDC, bcolors.WARNING + "", sum, "" + bcolors.ENDC, bcolors.CYAN + "\t Ship capacity left (persons):" + bcolors.ENDC, bcolors.WARNING + "", ship.cap, "" + bcolors.ENDC)
            ship.cap = whole_cap
            ship.x = start_xpos
            ship.y = start_ypos
        plt.show()
    mission_overview(sum, saved_points)
    return saved_points

# Finds the shortest route by saving as many people as possible in as little time as possible


def astar_algorithm(areas_centers, people_endangered, ship1, ship2, ship3, port_x, port_y):
    pass


def mission_overview(remaining, savedp):
    print("\n Mission Result")
    print("===============")
    saved = 0
    for point in savedp:
        saved = saved + point.closeby
    print("People saved:      \t", saved)
    print("People left behind: \t", remaining)
    print("Established in [s]:")
    print("Proclaimed:         Successfull")
# This function converts velocity to SI units


def vel_kn_to_ms(vel):
    vel_ms = vel * 0.5144
    return vel_ms

# This is the program's main module and gets executed first

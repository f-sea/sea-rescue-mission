'''----------------------------------------------------------------------------------------------
Needed Python libraries and modules
-------------------------------------------------------------------------------------------------'''
import pyfiglet
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import ion, show
import os
from util import *

show_animation = True
cluster_labels = []
cl_pos = []

'''---------------------------------------------------------------------------------------------
This module handles all of the algorithm's ploting
----------------------------------------------------------------------------------------------'''


def make_needed_plots(port_x, port_y, people_indanger, centerX, centerY, enc_circle_x, enc_circle_y, R_max_possible):
    ion()
    plt.style.use('dark_background')
    fig = plt.figure()
    plt.plot(port_x, port_y, 'yx')
    for person in people_indanger:
        if (person.id == 'cluster'):
            plt.plot(person.x, person.y, 'm,')
            an = plt.annotate(person.closeby, (person.x, person.y), fontsize=7)
            cluster_labels.append(an)
            cl_pos.append([person.x, person.y])
        else:
            plt.plot(person.x, person.y, 'r,')
    plt.plot(centerX, centerY, 'cx')
    plt.plot(enc_circle_x, enc_circle_y, 'b-.')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.axis('equal')
    plt.grid(color='g', linestyle='--', linewidth=2)
    plt.title('Mission overview')
    plt.show()
    plt.pause(0.0001)


'''---------------------------------------------------------------------------------------------------
Main function
---------------------------------------------------------------------------------------------------'''


def main(arguments):
    """Program executes with the following parameters:
    1. Ports coordinates--> port_x, port_y (point P)
    2. Wreck's coordinates--> wreck_x, wreck_y (point W)
    3. Maximum radius measured in reference to W in which people are floating on sea surface--> R
    4. Number of people onboard--> N
    5. People that were not saved in case of an existing wreck with known casualties--> Ncas [optional]
    6. Water state (w for warm, c for cold). If not specified, warm water conditions are going to be considered

    Algorithm call format: python3 ports.py port_x port_y wreck_x wreck_y R N [Ncas Wstate]--optional
    Refer to help to view this documentation
    """
    # Print ASCII header
    ascii_banner = pyfiglet.figlet_format("Sea Rescue Mission")
    if (os.name == 'posix'):
        print(bcolors.CYAN + ascii_banner + bcolors.ENDC)
        print (bcolors.BOLD + bcolors.OKBLUE + "Develloped by:" + bcolors.ENDC + bcolors.ENDC)
        print (bcolors.BOLD + "Nick Kougiatsos -N.A.M.E" + bcolors.ENDC)
        print (bcolors.BOLD + "Dimitris Tsoumpelis -N.A.M.E" + bcolors.ENDC + "\n")
    else:
        print(ascii_banner)
        print ("Develloped by:")
        print ("Nick Kougiatsos -N.A.M.E")
        print ("Dimitris Tsoumpelis -N.A.M.E \n")

    # Arguments placing
    l = []
    try:
        f = open('input.txt', 'r')
    except:
        print('No input file present!')
        print('Exiting now...')
        exit()
    for line in f:
        l.append(line.split('#')[0].split())
    port_x = float(l[0][0])
    port_y = float(l[1][0])
    wreck_x = float(l[2][0])
    wreck_y = float(l[3][0])
    R_max_possible = float(l[4][0])  # Distance in which there might lay passengers after the wreck [m]
    people_on_board = int(l[5][0])  # Defines number of points to be generated
    ii = 6
    try:
        people_dead = int(l[ii][0])  # The algorithm's minimum goal
        ii = ii + 1
    except:
        pass

    try:
        if (arguments[ii] == 'c'):
            human_endurance_water_seconds = 30 * 60  # The average human can last nearly for 30 minutes in cold water [s]
        elif (arguments[ii] == 'w'):
            human_endurance_water_seconds = 2 * 3600  # The average human can last nearly for 2 hours in relatively warm water [s]
    except:
        human_endurance_water_seconds = 2 * 3600  # The average human can last nearly for 2 hours in relatively warm water [s]
    #----------------------------------------------------------------------------------------------------------------------------------
    # Phase one: Determine and rank fleet according to saving efficiency
    #----------------------------------------------------------------------------------------------------------------------------------

    all_ships = getfleet(port_x, port_y)
    #----------------------------------------------------------------------------------------------------------------------------------
    # Phase two: Determine and categorize people in danger (clusters and solitairies)
    #----------------------------------------------------------------------------------------------------------------------------------

    people_indanger = []  # Stores all the object-type data generated by the people_in_danger class
    # Generate random points in defined radius
    for person in range(1, people_on_board):
        r = R_max_possible * np.random.random()
        theta = np.random.random() * 2 * np.pi
        x = wreck_x + r * np.cos(theta)
        y = wreck_y + r * np.sin(theta)
        person_indanger = people_in_danger(x, y)
        people_indanger.append(person_indanger)

    people_indanger = process_points(people_indanger)
    #----------------------------------------------------------------------------------------------------------------------------------
    # Topology needed
    #----------------------------------------------------------------------------------------------------------------------------------

    theta = np.arange(0, 2 * np.pi, 0.1)    # Generate encompassing circle circumference points
    enc_circle_x = wreck_x + R_max_possible * np.cos(theta)
    enc_circle_y = wreck_y + R_max_possible * np.sin(theta)
    #-----------------------------------------------------------------------------------------------------------------------------------
    # The function responsible for all the plotting is seizing control
    #-----------------------------------------------------------------------------------------------------------------------------------

    make_needed_plots(port_x, port_y, people_indanger, wreck_x, wreck_y, enc_circle_x, enc_circle_y, R_max_possible)
    #-----------------------------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------------------------
    # The user is prompted to select a solving algorithm
    #----------------------------------------------------------------------------------------------------------------------------------

    algorithm_selection = input(" Do you want to use Dijskra or A-star algorithm? (d/a) \n")
    if ((algorithm_selection == "d") or (algorithm_selection == "D")):
        dijskra_algorithm(people_indanger, all_ships, port_x, port_y, show_animation, human_endurance_water_seconds, cluster_labels, cl_pos)
    elif ((algorithm_selection == "a") or (algorithm_selection == "A")):
        astar_algorithm(people_indanger, all_ships, port_x, port_y)
    else:
        print(" There is no such algorithm. Please try again next time!")
        exit()
    #-----------------------------------------------------------------------------------------------------------------------------------


'''------------------------------------------------------------------------------------------------------------------------------
Direct control to main() --see above
------------------------------------------------------------------------------------------------------------------------------'''

if __name__ == '__main__':
    main(sys.argv)

#!---------------------------------------------------------------------------------------------------------------------------------

'''----------------------------------------------------------------------------------------------
Needed Python libraries and modules
-------------------------------------------------------------------------------------------------'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import ion, show
import os
import pandas as pd
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
        self.save_time = []
        self.mission_time=0
        self.lives_saved_before_critical = []
        self.cap_left = cap

    def getefficiency(self):
        """Each ship's capability is measured as the product of its capacity and its velocity"""
        self.score = self.cap * self.vel
        eff = self.score
        return eff

    def time_to_save(self):
        self.save_time.append(self.distance_covered / self.vel)



class people_in_danger:  # Info by special tranceiver embedded in life jacket
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.closeby = 1
        self.id = 'solitary'
        self.cost = np.Infinity
        self.path = None
        self.visited = False


class coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.closeby=1


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
            #plt.annotate(person.closeby, (person.x, person.y), fontsize=7)
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



# Ship fleet setting and ranking


def getfleet(port_x, port_y):
    all_ships = []
    # Rescue fleet available by port (is set to be random in each run)
    if (os.name=='posix'):
        print(bcolors.UNDERLINE + "Case study's total ship fleet \n" + bcolors.ENDC)
    else:
        print("Case study's total ship fleet \n")
    ship1 = ships('Maya 850', vel_kn_to_ms(25), 17, port_x, port_y, np.random.randint(1, 10))  # Maya 850 by Norsafe
    ship2 = ships('Matrix 450', vel_kn_to_ms(6), 6, port_x, port_y, np.random.randint(1, 10))  # Matrix 450 by Norsafe
    ship3 = ships('FRC 1204', vel_kn_to_ms(35), 56, port_x, port_y, np.random.randint(1, 10))  # frc 1204 by fastrescuecraft.nl
    for ship in [ship1, ship2, ship3]:
        print(ship.id, ": \t", ship.no_total, '\n')
        all_ships.append(ship)
    return all_ships

# This function converts velocity to SI units

def vel_kn_to_ms(vel):
    vel_ms = vel * 0.5144
    return vel_ms

def organise_ships_by_job_efficiency(all_ships):
    all_eff = []
    for ship in all_ships:
        capab = ship.getefficiency()
        all_eff.append(capab)
    all_eff = np.asarray(all_eff)
    ind_sorted = np.argsort(all_eff)
    return ind_sorted

#--------------------------------------------------------------------------------------------------------------------------------

# Finds the shortest route by saving as many people as possible in as little time as possible

def two_opt_algorithm(nodes,show_animation,people_indanger,centerX,centerY,enc_circle_x,enc_circle_y,port_x,port_y,all_ships,human_endurance_water_seconds,people_dead,of):
    number_of_nodes=len(nodes)
    # Create an initial solution
    solution = [n for n in nodes]
    go = True
    # Try to optimize the solution with 2opt until
    # no further optimization is possible.
    while go:
        (go,solution) = optimize2opt(nodes, solution, number_of_nodes,show_animation,people_indanger,centerX,centerY,enc_circle_x,enc_circle_y,port_x,port_y)
    print ("Ship routing on progress...")
    results=ship_route(all_ships,solution,show_animation,human_endurance_water_seconds,people_dead,of)
    return results

#-----------------------------------------------------------------------------
#
#    Before 2opt             After 2opt
#       Y   Z                    Y   Z
#       O   O----->              O-->O---->
#      / \  ^                     \
#     /   \ |                      \
#    /     \|                       \
# ->O       O              ->O------>O
#   C       X                C       X
#
# In a 2opt optimization step we consider two nodes, Y and X.  (Between Y
# and X there might be many more nodes, but they don't matter.) We also
# consider the node C following Y and the node Z following X. i
#
# For the optimization we see replacing the edges CY and XZ with the edges CX
# and YZ reduces the length of the path  C -> Z.  For this we only need to
# look at |CY|, |XZ|, |CX| and |YZ|.   |YX| is the same in both
# configurations.
#
# If there is a length reduction we swap the edges AND reverse the direction
# of the edges between Y and X.
#
# In the following function we compute the amount of reduction in length
# (gain) for all combinations of nodes (X,Y) and do the swap for the
# combination that gave the best gain.
#

def optimize2opt(nodes, solution, number_of_nodes,show_animation,people_indanger,centerX,centerY,enc_circle_x,enc_circle_y,port_x,port_y):
    best = 0
    best_move = None
    # For all combinations of the nodes
    for ci in range(0, number_of_nodes):
        for xi in range(0, number_of_nodes):
            yi = (ci + 1) % number_of_nodes  # C is the node before Y
            zi = (xi + 1) % number_of_nodes  # Z is the node after X

            c = solution[ ci ]
            y = solution[ yi ]
            x = solution[ xi ]
            z = solution[ zi ]
            # Compute the costs of the four edges.
            [cy,ncost] = cost( c, y )
            [xz,ncost] = cost( x, z )
            [cx,ncost] = cost( c, x )
            [yz,ncost] = cost( y, z )

            # Only makes sense if all nodes are distinct
            if xi != ci and xi != yi:
                # What will be the reduction in length.
                gain = (cy + xz) - (cx + yz)
                # Is is any better then best one so far?
                if gain > best:
                    # Yup, remember the nodes involved
                    best_move = (ci,yi,xi,zi)
                    best = gain

    print ('Nodes on test:\t',best_move, '\t Cost minimized to:\t {:6.4f}'.format(best))
    if best_move is not None:
        (ci,yi,xi,zi) = best_move
        # This four are needed for the animation later on.
        c = solution[ ci ]
        y = solution[ yi ]
        x = solution[ xi ]
        z = solution[ zi ]

        # Create an empty solution
        new_solution = list(range(0,number_of_nodes))
        # In the new solution C is the first node.
        # This we we only need two copy loops instead of three.
        new_solution[0] = solution[ci]

        n = 1
        # Copy all nodes between X and Y including X and Y
        # in reverse direction to the new solution
        while xi != yi:
            new_solution[n] = solution[xi]
            n = n + 1
            xi = (xi-1)%number_of_nodes
        new_solution[n] = solution[yi]

        n = n + 1
        # Copy all the nodes between Z and C in normal direction.
        while zi != ci:
            new_solution[n] = solution[zi]
            n = n + 1
            zi = (zi+1)%number_of_nodes
        # Create a new animation frame
        frame4(nodes, new_solution, number_of_nodes, c, y, x, z, gain,show_animation,people_indanger,centerX,centerY,enc_circle_x,enc_circle_y,port_x,port_y)
        return (True,new_solution)
    else:
        return (False,solution)

iteration=0
def frame4(nodes, solution, sn, c, y, x, z, gain,show_animation,people_indanger,centerX,centerY,enc_circle_x,enc_circle_y,port_x,port_y):
    global iteration
    global nn
    [distance_total,l_min] = total_cost( nodes, solution )
    point_grid = [ (n.x,n.y) for n in solution ]
    point_grid = np.array( point_grid )

    point_grid2 = [ (c.x,c.y), (y.x,y.y) ]
    point_grid3 = [ (x.x,x.y), (z.x,z.y) ]
    point_grid2 = np.array( point_grid2 )
    point_grid3 = np.array( point_grid3 )
    if show_animation:
        plt.clf()
        plt.plot(point_grid[:,0],point_grid[:,1],'w-')
        plt.plot(port_x, port_y, 'yx')
        '''
        for person in people_indanger:
            if (person.id == 'cluster'):
                plt.plot(person.x, person.y, 'm,')
                #an = plt.annotate(person.closeby, (person.x, person.y), fontsize=7)
                #cluster_labels.append(an)
                #cl_pos.append([person.x, person.y])
            else:
                plt.plot(person.x, person.y, 'r,')
        '''
        plt.plot(centerX, centerY, 'cx')
        plt.plot(enc_circle_x, enc_circle_y, 'b-.')
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        plt.axis('equal')
        plt.grid(color='g', linestyle='--', linewidth=2)
        if gain < 0:
            plt.scatter(point_grid2[:,0], point_grid2[:,1],c='yellow')
            plt.plot(point_grid2[:,0],point_grid2[:,1],c='white',linewidth=2,alpha=0.3)
            plt.scatter(point_grid3[:,0], point_grid3[:,1],c='yellow')
            plt.plot(point_grid3[:,0],point_grid3[:,1],c='white',linewidth=2,alpha=0.3)
            plt.title('2-Opt Algorithm Selected \t Distance total: {:6.1f}'.format(distance_total))
        else:
            plt.scatter(point_grid2[:,0], point_grid2[:,1],c='yellow')
            plt.plot(point_grid2[:,0],point_grid2[:,1],c='white',linewidth=2,alpha=0.3)
            plt.scatter(point_grid3[:,0], point_grid3[:,1],c='yellow')
            plt.plot(point_grid3[:,0],point_grid3[:,1],c='white',linewidth=2,alpha=0.3)
            plt.title('2-Opt Algorithm Selected \t Distance total: {:6.1f}'.format(distance_total))
            iteration += 1
            print ("Iteration:",iteration)
        plt.show()
        plt.pause(0.0001)

def ship_route(all_ships,points_to_visit,show_animation,human_endurance_water_seconds,people_dead,of):
    ship_ranking = organise_ships_by_job_efficiency(all_ships)
    visited=[points_to_visit[0]]
    colors = ["m", "g", "y"]
    path_index=0
    for rk in ship_ranking:
        plt.pause(0.0001)
        ship = all_ships[rk]
        color = colors[rk]
        for jj in range(0, ship.no_total):
            saved_from_current_ship=0
            if (os.name == 'posix'):
                print(bcolors.BOLD + "Ship \t", ship.id, "(", jj + 1, "/", ship.no_total, ") \t takes over the mission" + bcolors.ENDC)
            else:
                print("Ship \t", ship.id, "(", jj + 1, "/", ship.no_total, ") \t takes over the mission")
            ship.no_on_port = ship.no_on_port - 1
            whole_cap = ship.cap
            surpassed_critical_point = False
            while ((ship.cap > 0) and (path_index!=(len(points_to_visit)-1))):
                start_xpos = ship.x
                start_ypos = ship.y
                path_index+=1
                saved_from_current_ship+=1
                destination = points_to_visit[path_index]
                visited.append(destination)
                ship.distance_covered = ship.distance_covered + np.sqrt((start_xpos - destination.x)**2 + (start_ypos - destination.y)**2)
                ship.cap = ship.cap - destination.closeby
                if (((ship.distance_covered/ship.vel+10*60*saved_from_current_ship) >= human_endurance_water_seconds) and (surpassed_critical_point == False)):
                    surpassed_critical_point = True
                    ship.lives_saved_before_critical.append(saved_from_current_ship)
                if show_animation:
                    plt.show()
                    plt.plot([ship.x, destination.x], [ship.y, destination.y], color + "-")
                    plt.pause(0.0001)
                ship.x = destination.x
                ship.y = destination.y
            sum1 = 0
            sum2=0
            for point in points_to_visit:
                sum1+= point.closeby
            for point in visited:
                sum2+=point.closeby
            if (os.name == 'posix'):
                print(bcolors.CYAN + "People left behind: \t" + bcolors.ENDC, bcolors.WARNING + "", sum1-sum2, "" + bcolors.ENDC, bcolors.CYAN + "\t Ship capacity left (persons):" + bcolors.ENDC, bcolors.WARNING + "", ship.cap, "" + bcolors.ENDC)
            else:
                print("People left behind: \t", sum1-sum2, "\t Ship capacity left (persons): \t", ship.cap)
            ship.time_to_save()
            ship.cap = whole_cap
            ship.distance_covered=0
            '''
            ship.x = start_xpos
            ship.y = start_ypos
            '''
        plt.show()
    results=mission_overview(all_ships, sum1-sum2, visited,people_dead,of)
    return results
    #return saved_points

def total_cost( nodes, solution ):
    """Compute the total distrance travelled for the given solution"""
    [total_distance,cost_objective] = cost( solution[-1], solution[0] )
    for index in range(0, len(solution)-1):
        [distance,new_cost]=cost(solution[index], solution[index+1])
        cost_objective += new_cost
        total_distance+=distance
    return [total_distance,cost_objective]

def cost(n1, n2):
    """Compute the distance between two nodes"""
    distance=np.sqrt( (n1.x - n2.x)**2 + (n1.y - n2.y)**2 )
    people_at_destination=n2.closeby
    route_cost=distance/people_at_destination
    return [distance,route_cost]


'''
/*Results*/
'''
def mission_time(ships):
    times = []
    lives_up_to_critical=0
    for ship in ships:
        max_mission_time=max(ship.save_time)
        times.append(max_mission_time)
        lives_up_to_critical+=sum(ship.lives_saved_before_critical)
    return [lives_up_to_critical, max(times)]

mission_overview_calls=0
def mission_overview(ships, remaining, savedp,people_dead,of):
    global mission_overview_calls
    mission_overview_calls+=1
    df=pd.DataFrame()
    of.write(str(mission_overview_calls)+'\t')
    for ship in ships:
        of.write(str(ship.no_total)+'\t'+str(ship.vel)+'\t'+str(ship.cap)+'\t'+str(ship.score)+'\t')
    '''
    columns = ['Run','Maya 450','Matrix 850','FRC 1204','Saved','Remaining','Time','Saves up to critical time','People Dead']
    df=pd.DataFrame()
    df.columns=columns
    df['Run'][mission_overview-1]=mission_overview

    for ship in ships:
        ship_column=ships.index(ship)+1
        if (ship_column==1):
            df['Maya 450'][mission_overview_calls-1]=ship.no_total
        elif (ship_column==2):
            df['Matrix 450'][mission_overview_calls-1]=ship.no_total
        else:
            df['FRC 1204'][mission_overview_calls-1]=ship.no_total
    '''
    print("\n Mission Result")
    print("===============")
    saved = 0
    for point in savedp:
        saved = saved + point.closeby
    of.write(str(saved)+'\t'+str(remaining)+'\t')
    '''
    df['Saved'][mission_overview_calls-1]=saved
    df['Remaining'][mission_overview_calls-1]=remaining
    '''
    print("People saved:      \t", saved,' p')
    print("People left behind: \t", remaining, ' p')
    [crit_lives, time] = mission_time(ships)
    '''
    df['Time'][mission_overview_calls-1]=(time+600*saved)/3600
    df['Saves up to critical time'][mission_overview_calls-1]=crit_lives
    df['People Dead'][mission_overview_calls-1]=people_dead
    '''
    of.write(str(format((time+600*saved)/3600, '.2f'))+'\t')
    of.write(str(crit_lives)+'\t'+str(people_dead)+'\n')
    print("Established in [h]: \t", format((time+600*saved)/3600, '.2f')) #10 minutes delay is also calculated between each save
    print("Lives saved before critical time: \t",crit_lives,' p')
    if (people_dead>=remaining):
        print("Proclaimed:\t Successfull")
    else:
        print ("Proclaimed:\t Failure")
    return df

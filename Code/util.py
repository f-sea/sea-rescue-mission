'''----------------------------------------------------------------------------------------------
Needed Python libraries and modules
-------------------------------------------------------------------------------------------------'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import ion, show
import os
import copy
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

def cost_list(idlist,points):
    cost=0
    for i in idlist:
        try:
            n=idlist[idlist.index(i)+1]
            cost=cost+np.sqrt((points[i].x-points[n].x)**2+(points[i].y-points[n].y)**2)
        except:
            pass
    return cost

def myFunc(e):
    return e[len(e)-1]

def calc_distance(ind_list1,ind_list2,shmeia): #pairnei san eisodo deiktes kai ypologizei thn apostash
    dist=np.sqrt((shmeia[ind_list1].x-shmeia[ind_list2].x)**2+(shmeia[ind_list1].y-shmeia[ind_list2].y)**2)
    return dist

def genetic_algo(nodes,show_animation,people_indanger,centerX,centerY,enc_circle_x,enc_circle_y,port_x,port_y,all_ships,human_endurance_water_seconds,people_dead,of):
    all_routes_costs=[]
    for generation in range(1,101):
        print("Generation:\t",generation)
        if (generation==1):
            #Construct individuals of first generation
            index_lists_set=shuffle(5,len(nodes))
            for id_list in index_lists_set:
                id_list.append(cost_list(id_list,nodes))
                print("Individual:\t",id_list)
            index_lists_set.sort(key=myFunc)
        else:
            next_generation=[index_lists_set[0],index_lists_set[1]]
            for i in range(0,2):
                next_generation=Mutation(next_generation[i],nodes)
            while(len(next_generation)!=len(index_lists_set)):
                [choices,b]=Choose_for_Cross(index_lists_set)
                candidate=Cross_Over(choices,0,1,0,nodes)
                candidate=Mutation(candidate,nodes)
        #mylist=Cross_Over(index_lists_set,0,1,0,nodes)
        #Mutation(nodes_lists_set)




def Cross_Over(deigmata,deigmata_index_0,deigmata_index_1,arxikos_deikths,shmeia):

    l1=[]
    i=arxikos_deikths
    fores_pou_l1_kenos=0
    next_gen=[i]

    while len(next_gen)<(len(deigmata[deigmata_index_0])-1):#vriskoume  th thesh tou stoixeiou i sthn kathe lista kai ti stoixei to perivalloun se
        a1=deigmata[deigmata_index_0].index(i)               #kathe lista, ypologizoume thn apostash metaksi twn stoixeiwn an den exoume hdh paei
        a2=deigmata[deigmata_index_1].index(i)
        if (a1==len(deigmata[deigmata_index_0])-2 ) :# an to a1 einai o teleutaios integer oi geitonikoi tou einai o prwtos kai o arxikos
            if (deigmata[deigmata_index_0][a1-1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][a1-1],calc_distance(i,deigmata[deigmata_index_0][a1-1],shmeia)])

            if (deigmata[deigmata_index_0][0] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][0],calc_distance(i,deigmata[deigmata_index_0][0],shmeia)])

        if (a1==0 ):
            if (deigmata[deigmata_index_0][1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][1],calc_distance(i,deigmata[deigmata_index_0][1],shmeia)])

            if (deigmata[deigmata_index_0][len(deigmata[0])-2] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][len(deigmata[0])-2],calc_distance(i,deigmata[deigmata_index_0][len(deigmata[0])-2],shmeia)])

        if (a2==len(deigmata[1])-2) :
            if (deigmata[deigmata_index_1][a2-1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][a2-1],calc_distance(i,deigmata[deigmata_index_1][a2-1],shmeia)])

            if (deigmata[deigmata_index_1][0] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][0],calc_distance(i,deigmata[deigmata_index_1][0],shmeia)])
                #print([deigmata[1][a2-1],calc_distance(i,deigmata[1][a2-1])
        if (a2==0 ):
            if (deigmata[deigmata_index_1][1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][1],calc_distance(i,deigmata[deigmata_index_1][1],shmeia)])

            if (deigmata[deigmata_index_1][len(deigmata[0])-2] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][len(deigmata[1])-2],calc_distance(i,deigmata[deigmata_index_1][len(deigmata[1])-2],shmeia)])

        if (a1>0 and a1<(len(deigmata[0])-2)):
            if (deigmata[deigmata_index_0][a1-1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][a1-1],calc_distance(i,deigmata[deigmata_index_0][a1-1],shmeia)])
                #print([deigmata[0][a1-1],calc_distance(i,deigmata[0][a1-1])])

            if (deigmata[deigmata_index_0][a1+1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][a1+1],calc_distance(i,deigmata[deigmata_index_0][a1+1],shmeia)])

        if (a2>0 and a2<(len(deigmata[1])-2)) :
            if (deigmata[deigmata_index_1][a2-1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][a2-1],calc_distance(i,deigmata[deigmata_index_1][a2-1],shmeia)])

            if (deigmata[deigmata_index_1][a2+1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][a2+1],calc_distance(i,deigmata[deigmata_index_1][a2+1],shmeia)])
        #print("to l1:",l1," next generation: ",next_gen)
        if len(l1)==0:#an exoume hdh paei se olous tous geitonikous deiktes tou i epilegoume enan tyxaia, pou den exume paei
            if fores_pou_l1_kenos==0 :
                a=deigmata[deigmata_index_1][0:(len(deigmata[deigmata_index_1])-1)]
                while ((i in next_gen)==True):
                    b=a.index(i)
                    a.pop(b)
                    i=rn.choice(a)
                fores_pou_l1_kenos+=1
            else :
                fores_pou_l1_kenos=+1
                while ((i in next_gen)==True):
                    b=a.index(i)
                    a.pop(b)
                    i=rn.choice(a)
            l1.append([i,1])

        l1.sort(key=myFunc) #vriskoume poios einai o geitonikos deikths tou i me thn mikroterh apostash
        i=l1[0][0]
        next_gen.append(i)
        #print(l1,"to_l1",",to_i:",i,next_gen)
        l1=[]
    return next_gen

                                                              #MUTATION

def Mutation(next_gen,shmeia): #oi listes den prepei na exoun sto telos to mhkos ths diadromhs
    gain=0
    k=0
    next_gener=copy.copy(next_gen)
    #print(next_gen)
    while gain<=0 and k<=30 :#sta teleutaia stadia mporei na einai diskolo na vrei veltiwsh kai na einai vary ypologistika, opote vazoume p.x. 30 epanalhpseis
        x1=np.random.randint(0,len(next_gener)-2) #epilegoume 2 shmeia apo to next gen
        x2=np.random.randint(0,len(next_gener)-2)
        while np.absolute(x2-x1)<=1 : #frontizoume na einai diaforetika shmeia
            x2=np.random.randint(0,len(next_gener)-2)
        y1=x1
        y2=x2
        x1=min(y1,y2) #to x1 na einai < x2
        x2=max(y1,y2)
        shm_C=next_gener[x1]
        shm_Y=next_gener[x1+1]
        shm_X=next_gener[x2]
        shm_Z=next_gener[x2+1]
        # to gain pou vriskei th diafora (CY+XZ)-(CX+YZ)
        gain=calc_distance(shm_C,shm_Y,shmeia)+calc_distance(shm_X,shm_Z,shmeia)-calc_distance(shm_C,shm_X,shmeia)-calc_distance(shm_Y,shm_Z,shmeia)
        if gain>0 :
            x_to_y_part=next_gener[x2:x1:-1]
            next_gener[x1+1:x2+1:1]=x_to_y_part
            #print("Mutated:",next_gen," x1:",x1," x2:",x2," gain:",gain)
            #print(x_to_y_part)
        k+=1

    return [next_gener,gain]

                         #Coosing From "deigmata" for Cross Over

def Choose_for_Cross(generation): #to kathe "list"-stoixeio tou generation exei sto telos to fitness tou
    num_of_elit=int(len(generation)*0.2) #prepei na exei toulaxiston 2 stoixeia ara len(generation)>=10

    elit_1=rn.randint(0,num_of_elit-1)
    elit_2=rn.randint(0,num_of_elit-1)
    bclass_1=rn.randint(num_of_elit,len(generation)-1)
    bclass_2=rn.randint(num_of_elit,len(generation)-1)
    while elit_2==elit_1 :#den prepei na epileksoume idious deiktes
        elit_2=rn.randint(0,num_of_elit-1)
    while bclass_2==bclass_1 :#den prepei na epileksoume idious deiktes
        bclass_2=rn.randint(num_of_elit,len(generation)-1)

    elist=[[elit_1]+generation[elit_1],[elit_2]+generation[elit_2]]#prosthetoume to [elit_1] gia na krathsoume th thesh ths listas me thn opoia tha ginei to Cross_Over
    elist.sort(key=myFunc)
    bclass=[[bclass_1]+generation[bclass_1],[bclass_2]+generation[bclass_2]]
    bclass.sort(key=myFunc)
    #print(elist,"<-elist bclass->",bclass)
    bias=0.7
    tyxaios=rn.random()

    if tyxaios<=bias :
        elit=elist[0][0]
    else:
        elit=elist[1][0]
    tyxaios=rn.random()

    if tyxaios<=bias :
        bclass=bclass[0][0]
    else:
        bclass=bclass[1][0]
    return (elit,bclass) #sto telos vgrazoume th thesh ths [lista] apo ta deigmata [[lista1],...,[listaN]]

                              #Creating form deigmata the next generation(!!)

def Next_Generation(deigmata,shmeia):#me vash to prohgoumeno generation vgazei to epomeno generation
    next_Generation=[]
    elit=int(len(deigmata)*0.2) #prepei na einai toulaxiston 2

    for i in range(elit):#vazoyme to prwto 20% me pithanothta mutation 0.01
        #print(deigmata[i])
        x=rn.random()
        prob_of_mutation=0.01 #mporoume na thn allaksoume
        if x<=prob_of_mutation :
            arxiko_cost_list=deigmata[i].pop(len(deigmata[i])-1)  #vgazoume to teleutaio stoixeio apo th lista giati "Mutation","Cross_Over" douleuoun mono me int
            mutant=Mutation(deigmata[i],shmeia)
            next_Generation.append(mutant[0]+[arxiko_cost_list-mutant[1]])
            deigmata[i]+[arxiko_cost_list]
        else:
            next_Generation.append(deigmata[i])

    bclass_num=len(deigmata)-elit

    for i in range(bclass_num):
        to_be_crossed=Choose_for_Cross(deigmata)
        crossing=Cross_Over(deigmata,to_be_crossed[0],to_be_crossed[1],0,shmeia)
        n_gen=crossing+[cost_list(crossing,shmeia)]
        next_Generation.append(n_gen)
    next_Generation.sort(key=myFunc)
    return next_Generation

def shuffle(how_many,no_nodes):
    set_of_lists=[]
    for counter in range(0,how_many+1):
        sing_index_list=[]
        for n in range(0,no_nodes):
            index=np.random.randint(0,no_nodes+1)
            while(index in sing_index_list):
                index=np.random.randint(0,no_nodes+1)
            sing_index_list.append(index)
        set_of_lists.append(sing_index_list)
    return set_of_lists

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
    solution.append(coordinates(port_x,port_y))
    solution.insert(0,coordinates(port_x,port_y))
    plt.plot([solution[0].x,solution[1].x],[solution[0].y,solution[1].y],'w-')
    plt.plot([solution[-1].x,solution[-2].x],[solution[-1].y,solution[-2].y],'w-')
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
    all_return_point=points_to_visit[-1]
    all_start_point=points_to_visit[0]
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
            ship.distance_covered = ship.distance_covered + np.sqrt((ship.x - all_return_point.x)**2 + (ship.y - all_return_point.y)**2)
            if show_animation:
                    plt.show()
                    plt.plot([ship.x, all_return_point.x], [ship.y, all_return_point.y], color + "-")
                    plt.pause(0.0001)
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
            ship.x = all_start_point.x
            ship.y = all_start_point.y
    mission_overview(all_ships, sum1-sum2, visited,people_dead,of)

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
    of.write(str(mission_overview_calls)+'\t')
    for ship in ships:
        of.write(str(ship.no_total)+'\t'+str(ship.vel)+'\t'+str(ship.cap)+'\t'+str(ship.score)+'\t')
    print("\n Mission Result")
    print("===============")
    saved = 0
    for point in savedp:
        saved = saved + point.closeby
    of.write(str(saved)+'\t'+str(remaining)+'\t')
    print("People saved:      \t", saved,' p')
    print("People left behind: \t", remaining, ' p')
    [crit_lives, time] = mission_time(ships)
    of.write(str(format((time+600*saved)/3600, '.2f'))+'\t')
    of.write(str(crit_lives)+'\t'+str(people_dead)+'\n')
    print("Established in [h]: \t", format((time+600*saved)/3600, '.2f')) #10 minutes delay is also calculated between each save
    print("Lives saved before critical time: \t",crit_lives,' p')
    if (people_dead>=remaining):
        print("Proclaimed:\t Successfull")
    else:
        print ("Proclaimed:\t Failure")


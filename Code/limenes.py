import numpy as np
#----------------------------------------Define required classes------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------


class ships:
    def __init__(self, myid, vel, cap, x_pos, y_pos, no):
        self.id = myid
        self.vel = vel
        self.cap = cap
        self.x = x_pos
        self.y = y_pos
        self.no_total = no
        self.no_on_port = no

    def are_available(self):
        if (self.no_on_port > 0):
            flag = 'available'
        else:
            flag = 'occupied'
        print(flag)

    def time_to_save(self, x):
        save_time = self.vel * x
        save_time_per_person = save_time / self.cap
        return save_time_per_person


class people_in_danger:  # Info by special tranceiver embedded in life jacket
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
#---------------------------------------------------------------------------------------------------------------------
#----------------------------------------Define required classes------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------


# Rescue fleet available by port
ship1 = ships('Matrix 450', 6 * 0.5144, 6, 3, 0, np.random.choice(5, 1))  # Matrix 450 by Norsafe
ship1.no_total
ship2 = ships('Maya 850', 25 * 0.5144, 17, 5, 0, np.random.choice(5, 1))  # Maya 850 by Norsafe
ship3 = ships('FRC 1204', 35 * 0.5144, 56, 10, 0, np.random.choice(5, 1))  # frc 1204 by fastrescuecraft.nl
# ship1.are_available()
print("Case study's total ship fleet \n")
for ship in [ship1, ship2, ship3]:
    print(ship.id, ": \t", ship.no_total, '\n')


human_endurance_water_minutes = 4 * 24 * 3600  # The average human can last nearly for 3-5 days in relatively warm water (sharks and dehydration-famine excluded)
ship1.time_to_save(4)

'''People distribution on sea . The accident happened 2 nautical miles out of Paros's port. There were a total of 533 passengers (fleet and normal)
81 people lost their lives   Source: https://www.news247.gr/afieromata/expres-samina-17-chronia-meta-to-nayagio-stin-paro-me-toys-81-nekroys.6519323.html'''
centerX = 1
centerY = 1
R_max_possible = 8
people_on_board = 533
x_pos = np.array([])
y_pos = np.array([])
for person in range(1, people_on_board):
    r = R_max_possible * np.sqrt(np.random.rand())
    theta = np.random.rand() * 2 * np.pi
    x = centerX + r * np.cos(theta)
    y = centerY + r * np.sin(theta)
    np.append(x_pos, x)
    np.append(y_pos, y)

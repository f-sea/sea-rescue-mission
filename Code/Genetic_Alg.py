import numpy as np
import random as rn
import scipy as sp
"""
1) O pinakas "shmeia" einai apla gia na exw kapoia grhgorh eisodo kai na vlepw an doulevei
sth thesh tou tha valoume ton pinaka "nodes" kai ta kosth mporoun na ypologistoun eite mono
me apostaseis eite kai diairontas me tous anthropous.

2) Ta shmeia (apo ton pinaka "shmeia") menoun stathera kai o kathe syndiasmos tous einai mia tyxai seira apo
to 0-size(shmeia,0)

3)o pinakas "deigmata" exei tis tyxaies seires apo shmeia. einai ths morfhs [[lista1],[lista2],...,[listaN]].
H kathe [lista] exei tous akeraious pou mas deixnoun tis theseis twn shmeiwn apo ton pinaka "shmeia" kai sto telos 
exei thn synolikh apostash ths diadromhs, P.X. [0,2,4,1,5,3.139439]. 

4) (Mallon to ksereis) Autes einai oi synarthseis gia to "util.py" sto "ports.py" tha tis kaloume gia na
vgoun oi nees genies kai ta loipa 
"""
def calc_distance(ind_list1,ind_list2): #pairnei san eisodo deiktes kai ypologizei thn apostash 
    dist=sp.sqrt((shmeia[ind_list1,0]-shmeia[ind_list2,0])**2+(shmeia[ind_list1,1]-shmeia[ind_list2,1])**2)
    return dist
def myFunc(e):
    return e[len(e)-1]
def cost_list(lista):
    cost=0
    for i in range(len(lista)-1):
        cost=cost+sp.sqrt((shmeia[lista[i],0]-shmeia[lista[i+1],0])**2+(shmeia[lista[i],1]-shmeia[lista[i+1],1])**2)
    return cost
N=15
deigmata=[]
a=range(N)
shmeia=np.random.random((N,2))


for i in range(6): # vgazoume 6 tyxaia deigmata tha to allaksoume meta, na valoume 60 as poume
    b=rn.sample(a,k=len(a)) #tyxaia seira akeraiwn 
    deigmata.append(b) 
    deigmata[i].append(cost_list(b))

deigmata.sort(key=myFunc) #katatasoume me vash th mikroterh apostash

                                                     #CROSS_OVER
def Cross_Over(deigmata_index_0,deigmata_index_1,arxikos_deikths):     
    
    l1=[]
    i=arxikos_deikths
    fores_pou_l1_kenos=0
    next_gen=[i]
    
    while len(next_gen)<(len(deigmata[deigmata_index_0])-1):#vriskoume  th thesh tou stoixeiou i sthn kathe lista kai ti stoixei to perivalloun se 
        a1=deigmata[deigmata_index_0].index(i)               #kathe lista, ypologizoume thn apostash metaksi twn stoixeiwn an den exoume hdh paei 
        a2=deigmata[deigmata_index_1].index(i)
        if (a1==len(deigmata[deigmata_index_0])-2 ) :# an to a1 einai o teleutaios integer oi geitonikoi tou einai o prwtos kai o arxikos
            if (deigmata[deigmata_index_0][a1-1] in next_gen)==False : 
                l1.append([deigmata[deigmata_index_0][a1-1],calc_distance(i,deigmata[deigmata_index_0][a1-1])])
                
            if (deigmata[deigmata_index_0][0] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][0],calc_distance(i,deigmata[deigmata_index_0][0])])

        if (a1==0 ):
            if (deigmata[deigmata_index_0][1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][1],calc_distance(i,deigmata[deigmata_index_0][1])])
                
            if (deigmata[deigmata_index_0][len(deigmata[0])-2] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][len(deigmata[0])-2],calc_distance(i,deigmata[deigmata_index_0][len(deigmata[0])-2])])

        if (a2==len(deigmata[1])-2) :
            if (deigmata[deigmata_index_1][a2-1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][a2-1],calc_distance(i,deigmata[deigmata_index_1][a2-1])])
                
            if (deigmata[deigmata_index_1][0] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][0],calc_distance(i,deigmata[deigmata_index_1][0])])
                #print([deigmata[1][a2-1],calc_distance(i,deigmata[1][a2-1])
        if (a2==0 ):
            if (deigmata[deigmata_index_1][1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][1],calc_distance(i,deigmata[deigmata_index_1][1])])
                
            if (deigmata[deigmata_index_1][len(deigmata[0])-2] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][len(deigmata[1])-2],calc_distance(i,deigmata[deigmata_index_1][len(deigmata[1])-2])])

        if (a1>0 and a1<(len(deigmata[0])-2)):
            if (deigmata[deigmata_index_0][a1-1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][a1-1],calc_distance(i,deigmata[deigmata_index_0][a1-1])])
                #print([deigmata[0][a1-1],calc_distance(i,deigmata[0][a1-1])])

            if (deigmata[deigmata_index_0][a1+1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_0][a1+1],calc_distance(i,deigmata[deigmata_index_0][a1+1])])

        if (a2>0 and a2<(len(deigmata[1])-2)) :        
            if (deigmata[deigmata_index_1][a2-1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][a2-1],calc_distance(i,deigmata[deigmata_index_1][a2-1])])

            if (deigmata[deigmata_index_1][a2+1] in next_gen)==False :
                l1.append([deigmata[deigmata_index_1][a2+1],calc_distance(i,deigmata[deigmata_index_1][a2+1])])

        if len(l1)==0: #an exoume hdh paei se olous tous geitonikous deiktes tou i epilegoume enan tyxaia, pou den exume paei
            if fores_pou_l1_kenos==0 :
                a=deigmata[deigmata_index_1][0:(len(deigmata[deigmata_index_1])-1)]
                while ((i in next_gen)==True):
                    b=a.index(i)
                    a.pop(b)
                    i=rn.choice(a)
                fores_pou_l1_kenos=+1
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

def Mutation(next_gen):
    x1=rn.randint(0,len(next_gen)-2) #epilegoume 2 shmeia apo to next gen 
    x2=rn.randint(0,len(next_gen)-2)
    while sp.absolute(x2-x1)<=1 : #frontizoume na einai diaforetika shmeia
        x2=rn.randint(0,len(next_gen)-1)
    y1=x1
    y2=x2
    x1=min(y1,y2) #to x1 na einai < x2
    x2=max(y1,y2)
    shm_C=next_gen[x1]
    shm_Y=next_gen[x1+1]
    shm_X=next_gen[x2]
    shm_Z=next_gen[x2+1]
    # to gain pou vriskei th diafora (CY+XZ)-(CX+YZ) 
    gain=calc_distance(shm_C,shm_Y)+calc_distance(shm_X,shm_Z)-calc_distance(shm_C,shm_X)-calc_distance(shm_Y,shm_Z)
    if gain>0 : 
        next_gen[x1+1]=shm_X
        next_gen[x2]=shm_Y
        if (x2-x1)>2:
            x_to_y_part=next_gen[x2-1:x1+1:-1]
            next_gen[x1+2:x2]=x_to_y_part
        print("Mutated:",next_gen," x1:",x1," x2:",x2," gain:",gain)
    else:
        print("Den egine Mutation")
    return next_gen

#dokimes
next_gen=Cross_Over(5,4,1)
print("Ektelesthke !! ",next_gen)
next_gen=Mutation(next_gen)
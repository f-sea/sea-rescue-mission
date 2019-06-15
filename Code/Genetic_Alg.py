import numpy as np
import random as rn
import scipy as sp
import copy
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
EXTRAS
1) oi synarthseis "calc_distance", "calc_list","Cross_Over","Mutation" exoun extra eisodo ta shmeia gia na mporoume na
elegxoume apo to main poia tha einai ta shmeia (nodes)
2)Allaxe ligo to "Mutation" wste na stamataei molis vrei mia veltiwsh me ton 2opt
3)Prostethike h "create_deigmata" gia na ftiaksei thn prwth generation
4)Prostethike h "Choose_for_Cross" pou epilegei listes apo to generation mexri twra gia na ginoun eisodos sthn "Cross_over"
5)Prostethike h "Next_Generation" pou paragei thn epomenh gennia me vash osa eipame
"""
def calc_distance(ind_list1,ind_list2,shmeia): #pairnei san eisodo deiktes kai ypologizei thn apostash 
    dist=sp.sqrt((shmeia[ind_list1,0]-shmeia[ind_list2,0])**2+(shmeia[ind_list1,1]-shmeia[ind_list2,1])**2)
    return dist

def myFunc(e):
    return e[len(e)-1]

def cost_list(lista,shmeia):
    cost=0
    for i in range(len(lista)-1):
        cost=cost+sp.sqrt((shmeia[lista[i],0]-shmeia[lista[i+1],0])**2+(shmeia[lista[i],1]-shmeia[lista[i+1],1])**2)
    return cost

def create_deigmata(N_deigm,N_shmeiwn):
    deigmata=[]
    a=range(N_shmeiwn)
    for i in range(N_deigm): # vgazoume 6 tyxaia deigmata tha to allaksoume meta, na valoume 60 as poume
        b=rn.sample(a,k=N_shmeiwn) #tyxaia seira akeraiwn 
        b.append(cost_list(b,shmeia))
        deigmata.append(b)

    deigmata.sort(key=myFunc) #katatasoume me vash th mikroterh apostash
    return deigmata

N=15
shmeia=np.random.random((N,2))
deigmata=create_deigmata(10,N)
                                                     #CROSS_OVER
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
        x1=rn.randint(0,len(next_gener)-2) #epilegoume 2 shmeia apo to next gen 
        x2=rn.randint(0,len(next_gener)-2)
        while sp.absolute(x2-x1)<=1 : #frontizoume na einai diaforetika shmeia
            x2=rn.randint(0,len(next_gener)-2)
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
        
#dokimes

mylist=Cross_Over(deigmata,0,1,0,shmeia)
print("Original_List:",mylist,"\nLenght:",len(mylist))
#print(deigmata[0],deigmata[1])
#x=Next_Generation(deigmata,shmeia)
#print("Choose_for_Cross(deigmata  ",Choose_for_Cross(deigmata))
mutant1=Mutation(mylist,shmeia)    # !!!!! h synarthsh Mutant allazei to orisma, giati??????
print("\nEktelesthke !!","\n After mutation mylist:",mylist,
      "\nAfter_Mutation mytant1:",mutant1,"\nLenght:",len(mutant1[0]))
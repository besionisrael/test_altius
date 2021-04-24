#! /usr/bin/env python 
# -*- coding: Latin-1 -*- 

  
from Tkinter import* #Bibliothèque graphique Python
from math import hypot,sqrt,floor  
from random import randrange 
from time import time 
from tkMessageBox import askokcancel #Message Box

def mise_en_place(): 
    "Initialisation de la mise en place de deux boules" 
    global flag,T,C,CS,M,d,x,y,dx,dy,F,ZERO,B,Cb
    flag=1 
    Bouton_mise_en_place.config(state=DISABLED)
    Bouton_lancer.config(state=ACTIVE)
    Bouton_lancer2.config(state=ACTIVE)
    #can.delete(ALL)
    T=time() # mémorisation de la valeur du temps au démarrage 
    M=2 # entrée du nombre de boules choisi, en prévision à un eventuelle amélioration du code
    
    
    #Variables opérationnelles:
         # x: liste des abscisses du coin supérieur gauche des boules 
         # y: liste des ordonnées du coin supérieur gauche des boules 
         # dx: Coefficient de lancement horizontal 
         # dy: Coefficient de lancement vertical
         # F : liste des couleurs (Rouge, Bleu ) X2

    x,y,dx,dy=[0],[0],[10, -10],[10,-10] # initialisation de ces quatre listes!
    #les valeurs données à dx et dy le sont en fonction de la première collision
    F=["red","blue", "red","blue"] 

    #Initialisation de l'emplacement de la boule rouge et bleu tel que défini dans le questionnaire
    x = [0, L-d]
    y = [L-d, L-d]
          
    # création d'une bibliothèque des boules: 
    B={} 
    # mise en place des boules: 
    for i in range(0,M):B[i+1]=can.create_oval(x[i],y[i],x[i]+d,y[i]+d,fill=F[i])
    #Fin de la mise en place

def lancer(): 
    "Question 1: mise en mouvement des boules et gestion des collisions" 
    global x,y,dx,dy,CC,C,CS,d,ZERO, initial, isQuestion2, initial2, CR, CB, CRB
    if flag==1 :
        Bouton_lancer.config(state=DISABLED)
        # mise en mouvement de la boule Bi, avec maintien dans les limites du tableau: 

        #Impulsion initiale pousser vers la droite pr B1 et vers la gauche pour B2  
        if initial:
            i = 0
            j = 1
            x[i],y[i]=x[i]+dx[i],y[i] # mise en mouvement de la boule B1 vers la droite
            x[j],y[j]=x[j]-dx[i],y[j] # mise en mouvement de la boule B2 vers la gauche
            can.coords(B[1],x[i],y[i],x[i]+d,y[i]+d)
            can.coords(B[2],x[j],y[j],x[j]+d,y[j]+d)
            
        else:
            #Dans le cas ou on est à un traitement initial relatif à la question 2
            if isQuestion2 and initial2:
                for i in range(0,2):#Fonctionnement normal pour B1 et B2                    
                        
                    x[i],y[i]=x[i]+dx[i],y[i]+dy[i] # mise en mouvement de la boule Bi 

                    #Gestion de rebond horizontal et vertical                
                    if x[i]>L-d:x[i],dx[i]=L-d,-dx[i] # rebond sur la bande droite 
                    if x[i]<0:x[i],dx[i]=0,-dx[i] # rebond sur la bande gauche 
                    if y[i]>H-d:y[i],dy[i]=H-d,-dy[i] # rebond sur la bande inférieure 
                    if y[i]<0:y[i],dy[i]=0,-dy[i] # rebond sur la bande supérieure '''

                    
                    can.coords(B[i+1],x[i],y[i],x[i]+d,y[i]+d) # nouvelles coordonnées de Bi 
                
                #Traitement initial pour B3 et B4
                x[2],y[2]=x[2]+dx[2],y[2] # mise en mouvement de la boule B3 vers la droite
                x[3],y[3]=x[3]-dx[2],y[3] # mise en mouvement de la boule B4 vers la gauche
                can.coords(B[3],x[2],y[2],x[2]+d,y[2]+d)
                can.coords(B[4],x[3],y[3],x[3]+d,y[3]+d)
            #Dans tous les autres cas: Cas normal!
            else: 
                for i in range(0,M):
                    
                        
                    x[i],y[i]=x[i]+dx[i],y[i]+dy[i] # mise en mouvement de la boule Bi 

                    #Gestion de rebond horizontal et vertical                
                    if x[i]>L-d:x[i],dx[i]=L-d,-dx[i] # rebond sur la bande droite 
                    if x[i]<0:x[i],dx[i]=0,-dx[i] # rebond sur la bande gauche 
                    if y[i]>H-d:y[i],dy[i]=H-d,-dy[i] # rebond sur la bande inférieure 
                    if y[i]<0:y[i],dy[i]=0,-dy[i] # rebond sur la bande supérieure '''

                    
                    can.coords(B[i+1],x[i],y[i],x[i]+d,y[i]+d) # nouvelles coordonnées de Bi 

        # gestion de la COLLISION entre Bj et Bi:              
        for i in range(1,M): 
            for j in range(0,i): 
                if j!=i: 
                    X,Y=x[j]-x[i],y[j]-y[i] 
                    Z=hypot(X,Y) # distance entre les centres de Bj et Bi 
                    if Z<=d: # si cette distance est inférieure au diamètre (d) 
                        C+=1 # il y a collision (incrémentation du compteur C)
                        if C == 1: 
                            #Afin de limiter l'impulsion de départ
                            initial = False
                            #SI ON EST DANS LE CAS DE LA QUESTION 2, introduire deux boules supplémentaires
                            if isQuestion2:
                                ajout_deux_boules()
                        elif C==2:
                            if isQuestion2:
                                initial2 = False
                        
                        if isQuestion2:
                            #Compte nombre de collision entre les boules rouges et bleus
                            #On sait que les rouges occupent position 0 et 2, les bleus 1 et 3
                            if ((i % 2) == 0) and ((j % 2) == 0):
                                CR += 1 #collision des rouges
                            elif((i % 2) != 0) and ((j % 2) != 0):
                                CB += 1
                            else:
                                CRB += 1
                        else:
                            #Pour la question 1, il n'y aura que des collisions rouges et bleus
                            CRB = C


                        CS=round(C/(time()-T+0.01),2) # calcul du nombre de collisions par seconde, depuis le départ 

                        # algorithme de calcul des nouvelles coordonnées de la boule B1 et B2
                        dX,dY=dx[j]-dx[i],dy[j]-dy[i] 
                        dZ=hypot(dX,dY) 
                        if dZ==0:m=0 # les vitesses sont nulles à l'arrêt du jeu
                        else:
                            k,K=dZ*dZ,X*dX+Y*dY 
                            m=(K+sqrt(K*K-k*(Z*Z-d*d)))/k 
                        x[i],y[i],x[j],y[j]=x[i]-m*dx[i],y[i]-m*dy[i],x[j]-m*dx[j],y[j]-m*dy[j] 
                        
                        
                        # algorithme de changement de direction des boules Bj et Bi après collision 
                        xx,xy,yy=X*X/Z/Z,X*Y/Z/Z,Y*Y/Z/Z 
                        dx[i],dy[i],dx[j],dy[j]=yy*dx[i]-xy*dy[i]+xx*dx[j]+xy*dy[j],-xy*dx[i]+xx*dy[i]+xy*dx[j]+yy*dy[j],xx*dx[i]+xy*dy[i]+yy*dx[j]-xy*dy[j],xy*dx[i]+yy*dy[i]-xy*dx[j]+xx*dy[j] 
                        

                        can.C.config(text='%s'%C) # visualisation du compteur de collisions (C) 
                        can.CS.config(text='%s'%CS) # visualisation du compteur de collisions par seconde (CS)
                        can.CR.config(text='%s'%CR) # visualisation du compteur de collisions  des rouges (CR) 
                        can.CB.config(text='%s'%CB) # visualisation du compteur de collisions des bleus (CB)
                        can.CRB.config(text='%s'%CRB) # visualisation du compteur de collisions mixtes (CRB)
        #gestion du trou dans les 4 coins

        
    root.after(10,lancer) 
 

def lancer2():
    ''' Extension Question 2 '''
    global isQuestion2, initial2
    isQuestion2 = True
    initial2 = True
    print("je suis là")
    lancer()

def ajout_deux_boules():
    #Initialisation de l'emplacement de la deuxième boule rouge et deuxième boule bleu tel que défini dans le questionnaire
    print("on est entré ?")
    global L, d, F, x, y, M, dx, dy
    M = 4

    print(dx, dy)

    x.append(0)
    x.append(L-d)
    y.append(L-d)
    y.append(L-d)
    dx.append(10)
    dx.append(-10)
    dy.append(10)
    dy.append(-10)
   
    #Mise en place aux places de base
    i = 2
    j = 3
    #B[3] = can.create_oval(Nx[0],Ny[0],Nx[0]+d,Ny[0]+d,fill=F[0])
    #B[4] = can.create_oval(Nx[1],Ny[1],Nx[1]+d,Ny[1]+d,fill=F[1])
    print(dx, dy)
    for i in range(2,M):
        print("i:", x[i],y[i])
        B[i+1]=can.create_oval(x[i],y[i],x[i]+d,y[i]+d,fill=F[i])



        


def stop(): 
    "" 
    global flag,d, L, H, x, y, dx, dy, initial
    flag=0 
    Bouton_mise_en_place.config(state=DISABLED)
    Bouton_lancer.config(state=DISABLED)
    can.delete(ALL) # effacement du contenu de la fenêtre
    create_table_view(can, L, H) 
    C=0;can.C.config(text='%s'%C)
    CS=0;can.CS.config(text='%s'%CS)
    texte=can.create_text(L/2,L/3,text='Fin de la simulation',fill="green")
    #x,y,dx,dy=[0],[0],[10, -10],[10,-10] # initialisation de ces quatre listes! 
    #initial = True
    #mise_en_place()

def quitter():
    ans=askokcancel('',"Voulez-vous réellement quitter ?")
    if ans:root.quit()

def create_table_view(can, L, H):
    for line in range(0, L, 100): # range(start, stop, step)
        can.create_line([(line, 0), (line, H)], fill='black', tags='grid_line_w')

    for line in range(0, H, 100):
        can.create_line([(0, line), (L, line)], fill='black', tags='grid_line_h')
    
######## Programme principal ############################################ 
  
# Création du widget principal : 
root = Tk() 
root.title('-------------Table de billard: Altius Technologies-------------------') 
#can = create_grid(root)  
# DONNEES INITALES : 
#Taille du tableau
n = 8
L= n * 100 # longueur du contenu graphique (on le multiplie par 100 pour une meilleur vue) 
H=L # largeur du tableau 
d=95 # diamètre de la boule 
initial = True
initial2 = False #Pr la question 2
isQuestion2 = False
M,C,CC,CR,CB,CRB=0,0,0,0,0,0 # compteurs de boules et de collisions 
flag=0 #Rendre les itérations sur la simulation possible
# création des widgets "dépendants" : 
can=Canvas(root,bg='white',height=H,width=L) 
#Créations des lignes de tableau
create_table_view(can, L, H)

can.grid(row=1,column=0,rowspan=2) 

can2=Canvas(root,bg='brown',highlightbackground='brown') 
can2.grid(row=1,column=1,sticky=N) 

Button(can2,text='Quitter la simulation !',command=quitter,bg="white").pack(side=BOTTOM)  
  
S=Button(can2,text='Stop !',height=2,width=25,relief=GROOVE,bg="white",activebackground="dark green",activeforeground="white",command=stop) 
S.pack(padx=5,pady=5,side=BOTTOM,anchor=SW) 
  
can.CS=Label(can2,text='0',fg='white',bg='brown') 
can.CS.pack(side=BOTTOM) 
Label(can2,text="Collisions par seconde",fg='white',bg='brown').pack(side=BOTTOM) 
  
can.C=Label(can2,text='0',fg='white',bg='brown') 
can.C.pack(side=BOTTOM) 
Label(can2,text="Nombre de collisions total",fg='white',bg='brown').pack(side=BOTTOM)


can.CR=Label(can2,text='0',fg='white',bg='brown') 
can.CR.pack(side=BOTTOM) 
Label(can2,text="Nombre de collisions entre rouges",fg='white',bg='brown').pack(side=BOTTOM)

can.CB=Label(can2,text='0',fg='white',bg='brown') 
can.CB.pack(side=BOTTOM) 
Label(can2,text="Nombre de collisions entre bleus",fg='white',bg='brown').pack(side=BOTTOM)

can.CRB=Label(can2,text='0',fg='white',bg='brown') 
can.CRB.pack(side=BOTTOM) 
Label(can2,text="Nombre de collisions mixtes (bleus et rouges)",fg='white',bg='brown').pack(side=BOTTOM)

Bouton_lancer2=Button(can2,text='Question 2: Lancez l\'algorithme !',height=2,width=25,relief=GROOVE,bg="white",activebackground="dark green",activeforeground="white",state=DISABLED,command=lancer2) 
Bouton_lancer2.pack(padx=5,pady=5,side=BOTTOM,anchor=SW) 
  
Bouton_lancer=Button(can2,text='Question 1: Lancez l\'algorithme !',height=2,width=25,relief=GROOVE,bg="white",activebackground="dark green",activeforeground="white",state=DISABLED,command=lancer) 
Bouton_lancer.pack(padx=5,pady=5,side=BOTTOM,anchor=SW) 

Bouton_mise_en_place=Button(can2,text='Mettre les 2 boules en place !',height=2,width=25,relief=GROOVE,bg="white",activebackground="dark green",activeforeground="white",state=ACTIVE,command=mise_en_place) 
Bouton_mise_en_place.pack(padx=5,pady=5,side=BOTTOM,anchor=SW) 



  

  
root.mainloop() 
root.destroy()   

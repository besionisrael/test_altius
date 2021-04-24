#! /usr/bin/env python 
# -*- coding: Latin-1 -*- 
# Python version 2.4.2 
# Tk version 8.4 
# IDLE version 1.1.2 
  

# "BILLARD Français", avec une amélioration pour contrer les phénomènes "d'adhérence". 
  
  
from Tkinter import* 
from math import hypot,sqrt,floor 
from random import randrange 
from time import time 
from tkMessageBox import askokcancel

def tirage(): 
    "mise en place d'un nombre variable de boules de couleurs différentes" 
    global flag,T,C,CS,M,d,x,y,dx,dy,F,ZERO,B,Cbn,vitesse
    flag=1 
    Bouton_tirage.config(state=DISABLED)
    Bouton_tirer.config(state=ACTIVE)
    can.delete(ALL)
    T=time() # mémorisation de la valeur du temps au démarrage 
    M=2 # entrée du nombre de boules choisi 
    if M<10:d=L/10 # limitation à L/10 du diamètre des boules pour M<10 
    else:d=L/(M+1) # le diamètre diminue en fonction du nombre de boules 
    
    # création de six LISTES: 
        # x: liste des abscisses du coin supérieur gauche des boules 
        # y: liste des ordonnées du coin supérieur gauche des boules 
        # dx: liste des vitesses horizontales des boules 
        # dy: liste des vitesses verticales des boules 
        # F: liste de 4 couleurs différentes 
        # vitesse: Définit la vitesse possible lors de l'execution de l'algo, Celui ci doit être déclarée
        # ZERO: liste de valeurs "zéro"

    vitesse = 10
    x,y,dx,dy=[L-d],[0],[vitesse],[vitesse] # initialisation (valeur du premier terme) de ces quatre listes 
    F=["blue","red","orange","black"] 
    ZERO=[0]  
    # extension aux termes de rangs suivants par la méthode "append" (qui allonge la liste,après le dernier terme): 
    # (les distributions en x,dx,dy sont aléatoires; celle en y est régulièrement répartie sur toute la hauteur du jeu) 
    for i in range(0,int(floor(M/2))):x.append(randrange(0,L/2-D/2-d));y.append(H/M*(i+1));dx.append(vitesse);dy.append(vitesse);F.append(F[i]);ZERO.append(0) 
    for i in range(int(floor(M/2)),M-1):x.append(randrange(L/2+D/2-d,L-d));y.append(H/M*(i+1));dx.append(vitesse);dy.append(vitesse);F.append(F[i]);ZERO.append(0) 
          
    # création d'une bibliothèque des boules: 
    B={} 
    # mise en place des boules: 
    for i in range(0,M):B[i+1]=can.create_oval(x[i],y[i],x[i]+d,y[i]+d,fill=F[i]) 
    #Cb=can.create_oval(L/2-D/2,H/2-D/2,L/2+D/2,H/2+D/2,outline="white") # cercle blanc au centre du jeu 

def tirer(): 
    "mise en mouvement de l'ensemble des boules et gestion des collisions" 
    global x,y,dx,dy,CC,C,CS,d,ZERO
    vitesse = 10
    if flag==1 :
        Bouton_tirer.config(state=DISABLED)
        # mise en mouvement de la boule Bi, avec maintien dans les limites du jeu: 
        for i in range(0,M): 
            x[i],y[i]=x[i]+dx[i],y[i]+dy[i] # mise en mouvement de la boule Bi 
            dx[i],dy[i]=f*dx[i],f*dy[i] # freinage (f) 

            if dx==ZERO and dy==ZERO:stop() # arrêt lorsque toutes les vitesses sont nulles
            if hypot(dx[i],dy[i])<s: dx[i],dy[i]=0,0 # immobilisation lorsque la vitesse devient inférieure au seuil (s) 
            if x[i]>L-d:x[i],dx[i]=L-d,-dx[i] # rebond sur la bande droite 
            if x[i]<0:x[i],dx[i]=0,-dx[i] # rebond sur la bande gauche 
            if y[i]>H-d:y[i],dy[i]=H-d,-dy[i] # rebond sur la bande inférieure 
            if y[i]<0:y[i],dy[i]=0,-dy[i] # rebond sur la bande supérieure 

            can.coords(B[i+1],x[i],y[i],x[i]+d,y[i]+d) # nouvelles coordonnées de Bi 
        
        # gestion de la COLLISION entre Bj et Bi: 
        for i in range(1,M): 
            for j in range(0,i): 
                if j!=i: 
                    X,Y=x[j]-x[i],y[j]-y[i] 
                    Z=hypot(X,Y) # distance entre les centres de Bj et Bi 
                    if Z<=d: # si cette distance est inférieure au diamètre (d) 
                        C+=1 # il y a collision (incrémentation du compteur C) 
                        CS=round(C/(time()-T+0.01),2) # calcul du nombre de collisions par seconde, depuis le départ 

                        # algorithme de recul de Bj et Bi, sur leurs directions initiales, pour revenir au stricte contact Bj/Bi:
                        # calcul de la vitesse après collision, pour l'instant laissons cela constant 
                        dX,dY=vitesse,vitesse
                        dZ=hypot(dX,dY) 
                        if dZ==0:m=0 # les vitesses sont nulles à l'arrêt du jeu
                        else:
                            k,K=dZ*dZ,X*dX+Y*dY 
                            m=(K+sqrt(K*K-k*(Z*Z-d*d)))/k 
                        x[i],y[i],x[j],y[j]=x[i]-m*dx[i],y[i]-m*dy[i],x[j]-m*dx[j],y[j]-m*dy[j] 
                        
                        # deuxième passage de cet algorithme: 
                        # (une étude de la cinématique de la collision montre qu'après un "stricte contact", suivi du changement de direction des boules, 
                        # il peut exister des cas de figure où l'on se retrouve avec Z<d au coup suivant; 
                        # il s'en suit un phénomène d'adhérence, pouvant aller jusqu'à leur immobilisation temporaire. 
                        # Pour résoudre ce probléme, aussi simplement que possible, on a pris le parti de procéder à un recul supplémentaire pour revenir à Z>d) 
                        X,Y=x[j]-x[i],y[j]-y[i] 
                        Z=hypot(X,Y) 
                        if Z<=d: 
                            if dZ==0:m=0
                            else:
                                k,K=dZ*dZ,X*dX+Y*dY 
                                m=(K+sqrt(K*K-k*(Z*Z-d*d)))/k 
                            x[i],y[i],x[j],y[j]=x[i]-m*dx[i],y[i]-m*dy[i],x[j]-m*dx[j],y[j]-m*dy[j] 
  
                        # algorithme de changement de direction des boules Bj et Bi après collision 
                        xx,xy,yy=X*X/Z/Z,X*Y/Z/Z,Y*Y/Z/Z 
                        dx[i],dy[i],dx[j],dy[j]=yy*dx[i]-xy*dy[i]+xx*dx[j]+xy*dy[j],-xy*dx[i]+xx*dy[i]+xy*dx[j]+yy*dy[j],xx*dx[i]+xy*dy[i]+yy*dx[j]-xy*dy[j],xy*dx[i]+yy*dy[i]-xy*dx[j]+xx*dy[j] 
  
                        can.C.config(text='%s'%C) # visualisation du compteur de collisions (C) 
                        can.CS.config(text='%s'%CS) # visualisation du compteur de collisions par seconde (CS) 
        
    root.after(10,tirer) 
 
def stop(): 
    "" 
    global flag,d
    flag=0 
    Bouton_tirage.config(state=ACTIVE)
#    Bouton_tirer.config(state=ACTIVE)
    can.delete(ALL) # effacement du contenu de la fenêtre 
    C=0;can.C.config(text='%s'%C)
    CS=0;can.CS.config(text='%s'%CS)
    texte=can.create_text(L/2,L/3,text='Fin de la simulation',fill="white") 
    d=d

def quitter():
    ans=askokcancel('',"Voulez-vous réellement quitter ?")
    if ans:root.quit()

######## Programme principal ############################################ 
  
# Création du widget principal : 
root = Tk() 
root.title('-------------Table de billard: Altius Technologies-------------------') 
  
# données initiales: 
L=800 # longueur du jeu 
H=L # largeur du jeu 
d=50 # diamètre de la première boule 
D=L/6 # diamètre du cercle blanc
f,s=0.999,0.3 # coefficient de freinage et seuil d'arrêt 
M,C,CC=0,0,0 # compteurs de boules et de collisions 
flag=0 
# création des widgets "dépendants" : 
can=Canvas(root,bg='dark green',height=H,width=L) 
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
Label(can2,text="Nombre de collisions",fg='white',bg='brown').pack(side=BOTTOM) 
  
Bouton_tirer=Button(can2,text='Lancez l\'algorithme !',height=2,width=25,relief=GROOVE,bg="white",activebackground="dark green",activeforeground="white",state=DISABLED,command=tirer) 
Bouton_tirer.pack(padx=5,pady=5,side=BOTTOM,anchor=SW) 
Bouton_tirage=Button(can2,text='Mettre les 2 boules en place !',height=2,width=25,relief=GROOVE,bg="white",activebackground="dark green",activeforeground="white",state=ACTIVE,command=tirage) 
Bouton_tirage.pack(padx=5,pady=5,side=BOTTOM,anchor=SW) 
  

  
root.mainloop() 
root.destroy()   

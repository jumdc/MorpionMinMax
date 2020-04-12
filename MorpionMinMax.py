"""
    MORPION
    MiniMax et AlphaBeta Search
    
    On considère que le bot joue 2, soit une croix 
        
"""

#Place le coup du bot le plus efficace
def MiniMax(s):
    #creer une copie de le grille pour simuler les coups du bot et du joueur et pas écraser la grille de jeu
    s2=[]
    for i in range(len(s)):
        temp=[]
        for j in range(len(s[i])):
            valeur=s[i][j]
            temp.append(valeur)
        s2.append(temp)
    #on cherche les premières actions possibles du bot 
    actions=Actions(s2)
    list_actions=[]
    for a in actions:
        #on place l'action et on simule le jeu qui peut en découler 
        x,y=a
        s2[x][y]=2
        util=Min(s2)
        list_actions.append([a,util])
        #une fois les simulations faites, on enlève l'action placée pour tester la suivante
        s2[x][y]=0
    #on classe la liste pas ordre d'utilité décroissante 
    list_actions.sort(key=lambda x: x[1],reverse=True)
    #le premièr élément de la liste correspond à l'action la plus stratégique
    action_final=list_actions[0][0]
    return action_final

def Max(s): # simule l'action du bot
    #on teste si l'état de la grille est terminal 
    fini,gagnant=TerminalTest(s)
    if fini==True:
        return Utility(s)
    else:
        #on suit l'algorithmique donnée
        #en copiant la grille pour les actions puissent être réversibles
        v=float('-inf')
        s2=[]
        for i in range(len(s)):
            temp=[]
            for j in range(len(s[i])):
                valeur=s[i][j]
                temp.append(valeur)
            s2.append(temp)
        actions=Actions(s2)
        for a in actions:
            v=max(v,Min(Result(s2,a)))
            s2=[]
            for i in range(len(s)):
                temp=[]
                for j in range(len(s[i])):
                    valeur=s[i][j]
                    temp.append(valeur)
                s2.append(temp)
        return v         

def Min(s): # on simule l'action du joueur
    #on teste si l'état de la grille est terminal 
    fini,gagnant=TerminalTest(s)
    if fini==True:
        return Utility(s)
    else:
        #on suit l'algorithmique donnée
        #en copiant la grille pour les actions puissent être réversibles
        v=float('inf')
        s2=[]
        for i in range(len(s)):
            temp=[]
            for j in range(len(s[i])):
                valeur=s[i][j]
                temp.append(valeur)
            s2.append(temp)
        actions=Actions(s2)
        for a in actions:                     
            v=min(v,Max(Result(s2,a)))
            s2=[]
            for i in range(len(s)):
                temp=[]
                for j in range(len(s[i])):
                    valeur=s[i][j]
                    temp.append(valeur)
                s2.append(temp)
        return v



#la fonction Actions(s) prend en argument un état du jeu soit une grille 
#et retourne toutes les coordonnées des cases soit les actions possibles
def Actions(s):
    listeActions=[]
    for i in range(0,3):
        for j in range(0,3):
            if s[i][j] == 0:
                listeActions.append([i,j])
    return listeActions

#la fonction Result(s,a) prend en argument un état du jeu soit une grille et une action 
#et place l'action de coordonnées a sur s
#selon l'état de la grille, place soit une action du bot soit une action pour le joueur
#retourne la grille complétée avec l'action jouée
def Result(s,a):    
    x=a[0]
    y=a[1]
    comptX=0
    comptO=0
    for i in range(0,3):
        for j in range(0,3):
            if s[i][j]==1:
                comptO+=1
            elif s[i][j]==2:
                comptX+=1
    if comptO>=comptX:
        s[x][y]=2
    else:
        s[x][y]=1
    return s

#TerminalTest : prend en argument un état s
#retourne True : si un des 2 joueurs a gagné ou si il n'y a plus de cases vides
def TerminalTest(s):
    fini=False
    gagnant=0
    nb0=0
    for i in range(0,3):
        for j in range(0,3):
            if s[i][j]==0:
                nb0+=1
    if s[0][0]==s[0][1]==s[0][2]!=0: #ligne 1
        fini=True
        gagnant=s[0][0]
    elif s[0][0]==s[1][1]==s[2][2]!=0: #diag gauche
        fini=True
        gagnant=s[0][0]
    elif s[0][2]==s[1][1]==s[2][0]!=0: #diag droite
        fini=True
        gagnant=s[0][2]
    elif s[1][0]==s[1][1]==s[1][2]!=0: #ligne 2
        fini=True
        gagnant=s[1][0]
    elif s[2][0]==s[2][1]==s[2][2]!=0: #ligne 3
        fini=True
        gagnant=s[2][0]
    elif s[0][0]==s[1][0]==s[2][0]!=0: #colonne 1 
        fini=True
        gagnant=s[0][0]
    elif s[0][1]==s[1][1]==s[2][1]!=0: #colonne 2
        fini=True 
        gagnant=s[0][1] 
    elif s[0][2]==s[1][2]==s[2][2]!=0: #colonne 3
        fini=True
        gagnant=s[0][2] 
    elif nb0==0:
        fini=True  
    return fini,gagnant

#Utility prend en argument un état s
#elle assigne l'utilité à chaque grille étant en Terminal Test TRUE
#si elle pleine sans vainqueur: 0
#si le bot gagne: 1
#si le joueur gagne:-1
#retournne cette utilité en int
def Utility(s):
    fini,gagnant=TerminalTest(s)
    util=0
    if fini==True:
        if gagnant==1:
            util=-1
        #on faisait un else et non un elif gagnant ==2, du coup si la grille était fini mais que personne n'avait gagngé
        #le gagnant était quand même considéré comme étant 2
        elif gagnant==2:
            util=1
    return util



#Place le coup du bot le plus efficace
#mais cette fois en introduit un élagage de type alpha beta
def AlphaBetaSearch(s):
    inf=float("inf")
    minf=float("-inf")
    s2=[]
    for i in range(len(s)):
        temp=[]
        for j in range(len(s[i])):
            valeur=s[i][j]
            temp.append(valeur)
        s2.append(temp)
    actions=Actions(s2)
    list_actions=[]
    for a in actions:
        #on place l'action et on simule le jeu qui peut en découler 
        x,y=a
        s2[x][y]=2
        util=MinValue(s2,minf,inf)
        list_actions.append([a,util])
        #on enlève l'action pour simuler l'action possible suivante
        s2[x][y]=0
    #on trie la liste des actions possibles selon l'utilité dans l'ordre décroissant
    #pour avoir l'action correspondante à l'utilité la plus stratégique 
    list_actions.sort(key=lambda x: x[1],reverse=True)
    action_final=list_actions[0][0]
    return action_final

#simule l'action du bot
#on introduit l'élagage alpha beta
#on suit l'algo alphabeta
def MaxValue(s,al,b):
    fini,gagnant=TerminalTest(s)
    if fini==True:
        return Utility(s)
    else:
        v=float('-inf')
        s2=[]
        for i in range(len(s)):
            temp=[]
            for j in range(len(s[i])):
                valeur=s[i][j]
                temp.append(valeur)
            s2.append(temp)
        actions=Actions(s2)
        res=[]
        for a in actions:
            #print("pour l'action dans MAX",a)
            mv=MinValue(Result(s2,a),al,b)
            v=max(v,mv)
            if v >= b:
                return v
            al=max(al,v)
            #reinit pas la grille après avoir descendu un path, teste sur une grille pleine
            res.append((a,v))
            s2=[]
            for i in range(len(s)):
                temp=[]
                for j in range(len(s[i])):
                    valeur=s[i][j]
                    temp.append(valeur)
                s2.append(temp)
        return v        

#simule l'action du joueur
#on introduit l'élagage alpha beta
#on suit l'algo alphabeta
def MinValue(s,al,b):
    fini,gagnant=TerminalTest(s)
    if fini==True:
        return Utility(s)
    else:
        v=float('inf')
        s2=[]
        for i in range(len(s)):
            temp=[]
            for j in range(len(s[i])):
                valeur=s[i][j]
                temp.append(valeur)
            s2.append(temp)
        actions=Actions(s2)
        for a in actions:
            mv=MaxValue(Result(s2,a),al,b)
            v=min(v,mv)
            if al >= v:
                return v
            b=min(b,v)
            s2=[]
            for i in range(len(s)):
                temp=[]
                for j in range(len(s[i])):
                    valeur=s[i][j]
                    temp.append(valeur)
                s2.append(temp)
        return v 

#affiche la grille
def affichage(s):
    print('-------')
    for i in s: 
        ligne='|'
        for j in i:
            if j==1:
                ligne+='O';
            elif j==2:
                ligne+='X'
            elif j==0:
                ligne+=' '
            ligne+='|'
        print(ligne)
        print('-------')         
         
#fonction pour joueur au morprion avec la méthode minMax SANS élagage
def metMinMax():
    s=[
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    etat=False
    affichage(s)
    while etat==False:       
        print()
        a=MiniMax(s)
        s=Result(s,a)
        print("bot")
        affichage(s)
        print()
        etat,gagnant=TerminalTest(s)
        if etat==False:
            x=int(input("x >"))
            y=int(input("y >"))
            while(s[x][y]!=0) :
                print('saisie incorrect')
                x=int(input("x >"))
                y=int(input("y >"))
            s[x][y]=1
            affichage(s)
            etat,gagnant=TerminalTest(s)
    if gagnant==1 or gagnant==2:
        print("vainqueur",gagnant)
    else:
        print("pas de vainqueur")

#fonction pour joueur au morprion avec la méthode minMax AVEC l'élagage alphaBeta
def metAlphaBeta():
    s=[
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    etat=False
    affichage(s)
    while etat==False:       
        print()
        a=AlphaBetaSearch(s)
        s=Result(s,a)
        print("bot")
        affichage(s)
        print()
        etat,gagnant=TerminalTest(s)
        if etat==False:
            x=int(input("x >"))
            y=int(input("y >"))
            while(s[x][y]!=0) :
                print('saisie incorrect')
                x=int(input("x >"))
                y=int(input("y >"))
            s[x][y]=1
            affichage(s)
            etat,gagnant=TerminalTest(s)
    if gagnant==1 or gagnant==2:
        print("vainqueur",gagnant)
    else:
        print("pas de vainqueur")
    
#le joueur peut choisir quelle méthode peut être utilisée
def main():
    print('Souhaitez-vous jouer avec la méthode MinMax ou avec AlphaBeta ?')
    x=int(input("1=MinMax ou 2=AlphaBeta > "))
    if x==1:
        metMinMax()
    elif x==2:
        metAlphaBeta()
    else:
        print('saisie incorrecte')

main()
import sqlite3
import matplotlib.pyplot as plt

class HotelDB :
    def __init__(self,fichier):
        self.__conn = sqlite3.connect(fichier)
        

    def get_name_hotel_etoile(self,nbEtoiles):
        try :
            curseur = self.__conn.cursor() 
            S=[]
            request="SELECT nom FROM hotel WHERE etoiles=" + str(nbEtoiles)
            for ligne in curseur.execute(request):
                S.append(ligne)
            return S
        except sqlite3.OperationalError :                                
            S=[]
            return S
    """
    def add_new_client(self,nom,prenom):
        curseur = self.__conn.cursor()
        try :
            request1= "SELECT numclient FROM client WHERE nom=" + nom + "AND prenom=" + prenom
            curseur.execute(request1)
        except sqlite3.OperationalError :
            print
            return None
        list=curseur.fetchall()
        if len(list) > 0 :
            print("Le client existe")
            return list[0]
        request2 = "INSERT INTO client(nom,prenom) VALUES(" + nom +"," + prenom +")"
        curseur.execute(request2)
        self.__conn.commit()
        return curseur. """

    def add_new_booking(self,num_Client,num_Hotel,date_Depart,date_Arrive):
        curseur = self.__conn.cursor()

        # Création de la liste des chambres occupés d'un hotel
        request1 = "SELECT DISTINCT numchambre FROM occupation WHERE numhotel = " + str(num_Hotel) + " AND (( datedepart >= '" + date_Arrive + "' AND datedepart <= '" + date_Depart + "') OR ( datearrivee >= '" + date_Arrive + "' AND datearrivee <= '" + date_Depart +"' ))"
        curseur.execute(request1)                      
        Liste_Chambres_Occupees = curseur.fetchall()  
        
        # Création de la liste de toutes les chambres  d'un hotel
        request2 = "SELECT numchambre FROM chambre WHERE numhotel = " + str(num_Hotel)
        curseur.execute(request2)
        Liste_Chambres = curseur.fetchall() 

        # Intersection des 2 listes = Chambres Disponibles
        for el in Liste_Chambres:
            if not el in Liste_Chambres_Occupees:

                # Affectaion de la 1ère chambre disponible au client
                request3 = "INSERT INTO reservation(numclient,numchambre,numhotel,datearrivee,datedepart) VALUES(" + str(num_Client) +"," + str(el) +"," + str(num_Hotel) +"," + date_Arrive +"," + date_Depart +")"
                curseur.execute(request3)
                self.__conn.commit()
                break

    def Best_Choice(self):
        curseur = self.__conn.cursor()  
        Liste_Prix_Moyen=[]
        Liste_Occupations=[]
        Liste_Rapports=[]  
        for i in range(1,13):     # Créatin de la liste des prix moyens de chaque hotel
            request = "SELECT AVG(prixnuitht) FROM chambre WHERE numhotel = " + str(i) 
            curseur.execute(request)
            M=curseur.fetchall()
            N=M[0][0]
            Liste_Prix_Moyen.append(N)
        for i in range(1,13):      # Créatin de la liste des nombres d'occupations dans chaque hotel
            request = "SELECT COUNT(numoccup) FROM occupation WHERE numhotel = " + str(i) 
            curseur.execute(request)
            M=curseur.fetchall()
            N=M[0][0]
            Liste_Occupations.append(N)
        self.__conn.close() 
        for i in range(12):       # Créatin de la liste des rapports Occupation/prix de chaque hotel
            Liste_Rapports.append(Liste_Occupations[i]/Liste_Prix_Moyen[i])
        return Liste_Rapports
        
    

    
    def __str__(self):
        pass
    
    def __del__ (self):
	    self.__conn.close() 

if __name__=='__main__':
    aHotelDB = HotelDB('hotellerie.db')
    

    # Quelques requêtes vues en classe.

	#nbEtoiles = 2
	#resultat0 = aHotelDB.get_name_hotel_etoile(nbEtoiles)
	#print("Liste des noms d'hotel", nbEtoiles, "étoiles : ", resultat)
    #resultat = aHotelDB.Ajouter(1,"Dupont","Marcel")
    #print(resultat)

    # Requête 2


    ListeHotels = [ i for i in range(1,13) ]
    ListesRapp = aHotelDB.Best_Choice()
    plt.plot( ListeHotels , ListesRapp )

    plt.title("Meilleur Hotel !!")

    plt.xlabel("Numeros D'hotels")
    plt.ylabel("Note")       # note = rapport nombre d'occupations/prix

    plt.show()
    plt.close()

   




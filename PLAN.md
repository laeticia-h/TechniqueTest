HAROUNA Laeticia M1 ILSEN

#INTRODUCTION

Le but de ce TP est de mettre en pratique un ensemble de tests afin de valider et
mesurer la fiabilité de l'algorithme, la justesse, la performance et la qualité de 
l'implémentation de Triangulator. Pour ce projet, nous allons utiliser une approche TDD
(Test Driven Development), on écrit les tests avant le code.

#CHOIX DE L'ALGORITHME DE TRIANGULATION

Pour l'algorithme de Triangulation, il est possible de choisir plusieurs
implémentations différentes : Diviser pour régner, algorithme incrémental,
plus proche voisin, basculement.

Mon choix va se porter sur l'algorithme Diviser pour régner car il est celui qui est le plus optimal 
et ne rencontre pas de "problème" par rapport aux algorithmes cités : 
	- Le problème de l'algorithme du plus proche voisin est qu'il est possible qu'il ne trouve aucun point
et donc que le point se retrouve seul. 
	- Pour l'algorithme incrémental, il faut ajouter les points 1 par 1 dans un grand triangle, il faut 
ensuite à chaque fois que l'on ajoute un nouveau point, trouver dans quel triangle existant il se situe 
pour supprimer ceux en conflit pour ensuite créer les triangles.
	- Pour l'algorithme de basculement, il faut avoir un premier triangle sinon il ne fonctionne pas,
donc si j'ai une erreur dans mon premier triangle, l'algorithme ne fonctionnera pas correctement (erreurs ).

Je trouve donc plus simple l'algorithme Diviser pour régner car pour diviser ça sera simple et je rencontrerais des difficultés uniquement dans l'étape de Fusion.


#PERIMETRE

Pour ce TP, on se concentre sur le micro service Triangulator qui dépend de PointSetManager car
il récupère l'ensemble des points auprès de cette composante.
Pour les autres composantes tels que la base de données, le client, API 
on utilisera un Mock afin d'isoler chaque element pour les tester seul.


	

#PRINCIPE DE TRIANGULATION
- CAS : 3 points donne 1 triangle
        4 points ( quadrilatère) donne 2 triangles
		
|CAS GENERAL : 2n - 2 - h |
		avec n = nombre total de points et h = nombre de points du contour
		Exemple d'application du cas général : 
		h = 4
		n = 5 
		2 x 5 - 2 - 4 =  4 donc on aura 4 Triangles
		
		Exemple 3 points :
		h et n = 3
		2 x 3 - 2 - 3 =  1
		
		Exemple 4 points : 
		h et n = 4 
		2 x 4 - 2 - 4 = 2
		
- CAS IMPOSSIBLE : points au même endroit ou très proches, moins de 3 points, NotaNumber, point aligné	
h>n


#IDEE DE TEST 
	- Est-ce que le format est respecté pour PointSet ?
	- Est-ce que j'ai le bon nombre de points ?
	- Est-ce que ma chaîne est valide ?
	- Où est-ce que je récupère la donnée pour chaque composante ?
	
	
#TEST DE PERFORMANCE
Ces tests vont permettre de mesurer la vitesse d'execution et la consommation de ressources
du mesure selon des données variables

//Pourquoi ? :
Un algorithme qui fonctionne bien sur peu de points peut ne plus tenir la charge si on utilise une taille importante de données
car ce qui est rapide et léger avec 10 points ne le reste pas forcément avec 10 000 points
 
//Comment ? : 
- Utilisation d'un eu de données variables (3,10,100,1000,10000) 
- Mesurer le temps de conversion (encode/decode)
- Mesure le temps de calcul de triangulation
- Mesurer la consommation de ressources
	
#TEST API
Ces tests vont permettre de vérifier que le serveur Flask communique correctement avec PointSetManager

//Pourquoi ? : 
Isolation du Triangulator pour tester son fonctionnement et vérifiquer que tout marche

//Comment ? : 
- Lancement du serveur Flask
- Utilisation des mocks pour simuler les réponses de PointSetManager

//Scénario : 
- Le client envoie une requête GET de triangulation --> je dois recevoir : 200 
- Le service récupère le PointSet Binaire dans PointSetManager (mock)
- Le service calcule la triangulation à partir de PointSet
- Le service renvoie au client le résultat encodé. 


#TEST DE ROBUSTESSE
Ces tests visent à vérifier le comportement du service face à des situations inattendues.
Si le service échoue on doit savoir pour quelle raison.

//Pourquoi ? : 
Un service dont on a pas anticipé les problèmes n'est pas fiable


//Comment : 

//Cas de Scénario  : Robustesse entrée incorrecte
- Envoyer une requête avec un contenu vide
- Envoyer un flux malformé
- Envoyer le mauvais type de données

//Cas de Scénario : PointSetManager mocké
- Simuler un TimeOut
- Absence de réponse 
- Mettre un flux binaire incorrect

//Cas de Scénario : Données très importante
... ( à réfléchir)



#COUVERTURE DE TESTS
Bien d'avoir entre 90% et 100%.


#CAS D'ERRREURS
Chaque execption doit être traduite par un message clair pour le client 

PointSet inexistant --> 404 Not Found
TimeOut, Triangulation Failed, Erreur méthode HTTP  --> 500 Internal Server Error
PointSetManager sans réponse --> 503 Service Unavailable

#CAS DE SUCCES
PointSet Créé --> 201 Created
Triangulation algorithme --> 200 OK

#CAS DE TEST 
|Scénario 1 : Décoder un PointSet valide
On veut vérifier qu'avec un flux binaire qui respecte le formation on retrouve les points qu'il contient 

Entrées : un flux binaire de 3 points

Résultat attendu : une liste de 3 points avec les bonnes coordonnées
Format : [(1.0, 2.0), (3.5, 4.5), (0.0, 0.0)]


|Scénario 2 : Encoder un PointSet valide
On vérifie l'inverse donc à partir de la liste des points on reproduit le flux binaire au bon format 

Entrées : une liste de 3 points

Résultat attendu : un flux binaire de la bonne taille (4bytes pour le points + 3×8 bytes ici on a mis 3 car 3 points en entrées )
Format : bytes (pour vérifier on fait len de l'objet et on doit retrouver 28 (cas de l'exemple)

|Scénario 3 : Encode puis decode
On vérifie que encode décode sont cohérents 

Entrées : une liste de points peu importe la taille 

Résultat attendu : après encodage puis décodage, on retrouve les mêmes points
Format :  la liste de points obtenue à la fin doit être identique à la liste de points du début

|Scénario 4 : Encoder un résultat de triangulation
On produit un flux binaire qui respecte le format Triangles
(la partie PointSet, suivie du nombre de triangles, suivie des indices de chaque triangle).

Entrées : Une liste de points : [(0,0), (4,0), (4,4), (0,4)]
avec les triangles trouvés ( voir schéma pour comprendre)

(0,4)-------(4,4)
  | \          |
  |   \   T2   |
  | T1  \      |
  |       \    |
(0,0)-------(4,0)
T1 = triangle (0, 1, 3) coordonnées des points (0,0), (4,0), (0,4)
T2 = triangle (3, 1, 2) coordonnées des points (0,4), (4,0), (4,4)

Résultat attendu : On veut transformer ces deux informations en un seul fichier binaire (suite de bytes)
pour l'envoyer au client
Format : 
[nombre de points] + [tous les points] + [nombre de triangles] + [tous les triangles]
     4 bytes         n × 8 bytes            4 bytes                m × 12 bytes
	 n = nb de points et m = nb triangles

|Scénario 5 : Requête de triangulation réussie
On vérifie que les scénarios précédents fonctionnent bien ensemble c'est-à dire
Décoder un PointSet, encoder un résultat,l'algo de Triangulation
Entrées : un identifiant de PointSet valide, PointSetManager (mock) renvoie un PointSet correct.

Résultat attendu : code 200 + flux Triangles valide. (explication dans TestApi)

|Scénario 6 : Encoder un PointSet avec des coordonnées négatives
On veut vérifier que l'encodage et le décodage fonctionne avec des coordonnées négatives
car les coordonnées sont du type float donc ce cas là doit fonctionner

Entrées : une liste de points avec des coordonnées négatives [(-3.0, -2.0), (5.0, -1.5), (-4.0, 6.0)].

Résultat attendu : on retrouve exactement les mêmes points 
	
	
(Rappel : ne pas oublier les cas cités au dessus ( coder les tests des cas impossibles,des cas d'erreurs etc...))

#Utilisation des opérations

Utilisation de Make  : 
 make test : lance tous les tests (basé sur pytest)
 make unit_test : lance tous les tests sauf les tests de performance (basé sur pytest)
 make perf_test : lance uniquement les tests de performance (basé sur pytest)
 make coverage : génère un rapport de couverture de code (basé sur coverage)
 make lint : valide la qualité de code (basé sur ruff check)
 make doc : génère la documentation en HTML (basé sur pdoc3)
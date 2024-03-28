# Listes de jeux de données que vous pouvez utiliser pour tester l'outil
## Données géocodées issues du recensement des licences et clubs auprès des fédérations sportives agréées par le ministère chargé des sports (data.gouv.fr)
Lien: https://www.data.gouv.fr/fr/datasets/donnees-geocodees-issues-du-recensement-des-licences-et-clubs-aupres-des-federations-sportives-agreees-par-le-ministere-charge-des-sports/

En-tête des codes des départements: Département

En-tête des valeurs à afficher: Total


## Populations légales 2017 (INSEE)
Lien: https://www.insee.fr/fr/statistiques/4265429?sommaire=4265511

En-tête des codes des départements: CODDEP

En-tête des valeurs à afficher: PTOT


## Combiner les deux jeux de données pour calculer le pourcentage de la population inscrite dans un club de sport
Formule: ```(V[1]/V[2])*100``` (Les indices 1 et 2 sont arbitraires, si les données du dessus ne sont pas dans à ces indices, il faut les changer dans la formule)

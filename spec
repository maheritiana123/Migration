Spécifications techniques — Affectation de l’équipe gestionnaire par compte
1. Objectif
Permettre à l’utilisateur de définir une équipe gestionnaire différente pour chaque compte de service généré.
L’équipe gestionnaire ne sera plus portée globalement par la demande, mais directement par chaque compte.
2. Nouveau comportement du flux de création
Étape 1 — Informations du compte
L’utilisateur renseigne les informations générales du compte.
Le champ Équipe gestionnaire ne doit pas être renseigné à cette étape.
Étape 2 — Sélection des sites et des comptes
Pour chaque site sélectionné, l’application affiche une ligne correspondant au compte qui sera créé.
Une nouvelle colonne Équipe gestionnaire est ajoutée au tableau.
Exemple :
Site
Nom du compte
Équipe gestionnaire
DA
compte_test_DA
3D60
DJ
compte_test_DJ
1320
KJ
compte_test_KJ
3A10
L’utilisateur doit sélectionner une équipe gestionnaire pour chaque ligne.
La liste des équipes disponibles est alimentée par la configuration existante des équipes gestionnaires.
3. Règles de validation
Avant de passer à l’étape suivante, le système doit vérifier que :
chaque compte possède une équipe gestionnaire ;
l’équipe sélectionnée existe bien dans la liste des équipes gestionnaires autorisées ;
aucune ligne sélectionnée ne reste sans équipe gestionnaire.
Message d’erreur proposé :
Une équipe gestionnaire doit être renseignée pour chaque compte sélectionné.
4. Création des comptes
Lors de la création, chaque compte est traité indépendamment.
Pour chaque ligne sélectionnée :
Site sélectionné
Nom du compte généré
Équipe gestionnaire sélectionnée
Le compte est créé avec l’équipe gestionnaire associée à sa ligne.
Exemple :
compte_test_DA → équipe 3D60
compte_test_DJ → équipe 1320
compte_test_KJ → équipe 3A10
5. Modification de compte
Lors de la modification, l’équipe gestionnaire doit être modifiable compte par compte.
Si un compte est ajouté à un nouveau site, l’utilisateur doit obligatoirement renseigner l’équipe gestionnaire de ce nouveau compte.
6. Impacts techniques
L’évolution impacte :
le flux de création de compte ;
l’écran de sélection des sites/comptes ;
le modèle de données de la demande si l’équipe gestionnaire était stockée uniquement au niveau global ;
le traitement de création des comptes AD ;
le traitement de modification des comptes ;
les contrôles de validation.
7. Point important
Aucune séparation des équipes par environnement n’est nécessaire dans la configuration.
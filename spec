Spécifications techniques – Séparation des équipes gestionnaires par environnement
1. Objet
Cette évolution a pour objectif de limiter l'administration des comptes de service selon l'environnement des sites auxquels ils sont rattachés.
Aujourd'hui, un compte de service est créé depuis l'application de production et peut être associé à des sites appartenant à différents environnements. Les équipes gestionnaires ne sont pas différenciées par environnement.
L'objectif est de distinguer les équipes gestionnaires dédiées aux environnements TEST, RECETTE et PROD, afin qu'une équipe ne puisse administrer que les comptes correspondant à son environnement.
2. Existant
Configuration
Les équipes gestionnaires sont actuellement stockées dans la table CONFIGURATION via une unique entrée.
Clé
Valeur
ADMIN_TEAMS
Liste des équipes séparées par ";"
Exemple

ADMIN_TEAMS
1320;1430;3A10;3D60
Toutes les équipes sont considérées comme équivalentes.
Gestion des comptes
Lors de la création d'un compte de service :
une équipe gestionnaire est sélectionnée ;
un ou plusieurs sites sont associés au compte.
Aucune vérification n'est réalisée entre l'équipe gestionnaire sélectionnée et l'environnement des sites.
3. Evolution de la base de données
Le format actuel de stockage est conservé.
La configuration sera découpée en plusieurs entrées.
Clé
ADMIN_TEAMS_TEST
ADMIN_TEAMS_RECETTE
ADMIN_TEAMS_PROD
Chaque valeur conservera le format actuel.
Exemple

ADMIN_TEAMS_TEST

1320;1430;2950

ADMIN_TEAMS_RECETTE

3A10;3A20

ADMIN_TEAMS_PROD

3D60;3M20
L'ancienne clé ADMIN_TEAMS sera conservée durant la phase de migration puis supprimée une fois l'ensemble des traitements adaptés.
4. Détermination de l'environnement
L'environnement d'un compte sera déterminé à partir des sites qui lui sont associés.
Chaque site possède déjà une information permettant de connaître son environnement.
Aucune évolution de la table SITE n'est nécessaire.
5. Evolution des traitements
Création d'un compte
Lors de la création :
récupération des sites sélectionnés ;
détermination de leur environnement ;
récupération des équipes autorisées pour cet environnement ;
contrôle de l'équipe sélectionnée.
Si l'équipe n'appartient pas à l'environnement du ou des sites sélectionnés, la création est refusée.
Modification d'un compte
Les mêmes contrôles devront être réalisés lors de la modification.
En cas de changement de sites, la cohérence entre l'équipe gestionnaire et les nouveaux sites devra être vérifiée.
Administration des équipes
L'écran d'administration devra permettre de gérer indépendamment les équipes :
TEST
RECETTE
PROD
Chaque modification devra mettre à jour la clé de configuration correspondante.
6. Contrôles
Les contrôles devront être réalisés côté serveur.
Pour chaque site associé au compte :
déterminer son environnement ;
récupérer les équipes autorisées ;
vérifier que l'équipe sélectionnée appartient à cette liste.
En cas d'incohérence, le traitement devra être interrompu.
Exemple :

Equipe gestionnaire : 1320

Environnement autorisé :
TEST

Site sélectionné :
Production

=> Création refusée
7. Migration
Une reprise des données sera nécessaire.
Les équipes actuellement présentes dans ADMIN_TEAMS devront être réparties entre :
ADMIN_TEAMS_TEST
ADMIN_TEAMS_RECETTE
ADMIN_TEAMS_PROD
Cette répartition sera fournie par le métier.
8. Impacts
Cette évolution impacte :
la gestion de la configuration des équipes gestionnaires ;
l'administration des équipes ;
la création d'un compte de service ;
la modification d'un compte de service ;
les contrôles de validation côté serveur.
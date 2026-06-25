1. Objet de l’évolution
Cette évolution a pour objectif de séparer les équipes gestionnaires par environnement fonctionnel : TEST, RECETTE et PROD. La séparation doit garantir qu’un compte de service créé pour un environnement donné soit administré uniquement par les équipes gestionnaires autorisées pour cet environnement.
L’évolution concerne principalement le flux de création de compte, la modification des comptes existants, l’administration de la configuration et les contrôles métier associés.
Règle centrale : un compte suffixé _test doit être administré par les équipes TEST, un compte suffixé _recette par les équipes RECETTE, et un compte suffixé _prod par les équipes PROD.
2. Contexte technique et fonctionnel
L’application ASVC existe sur plusieurs environnements. Chaque environnement dispose de sa propre base de données et de sa propre table SITE. Les environnements applicatifs ne communiquent pas entre eux.
En revanche, les comptes de service sont créés dans un Active Directory commun. Un compte AD créé depuis un environnement peut donc être retrouvé et modifié depuis les autres environnements.
Actuellement, la liste des équipes gestionnaires n’est pas segmentée. Une même liste est utilisée pour l’administration des comptes, ce qui ne permet pas de limiter l’administration selon l’environnement cible du compte.
Architecture logique simplifiée :

        Application TEST      Application RECETTE      Application PROD
              |                     |                     |
              |                     |                     |
              +---------- Active Directory commun --------+
                             Comptes de service AD
3. Existant
3.1 Configuration des équipes gestionnaires
Les équipes gestionnaires sont actuellement stockées dans la table CONFIGURATION via une clé unique.
Table	Clé	Valeur
CONFIGURATION	ADMIN_TEAMS	Liste des codes équipes séparés par ';'
Exemple : ADMIN_TEAMS = 1320;1430;2950;3A10;3D60
3.2 Sites
Le choix des sites est réalisé dans l’étape 2 du formulaire de création. L’utilisateur coche un ou plusieurs sites sur lesquels le compte sera utilisé. Chaque site permet de déterminer l’environnement cible du compte à créer.
Dans l’existant, la liste des sites affichée dépend de l’environnement applicatif et de la table SITE locale. Le champ technique de la table SITE permettant de dissocier les sites sera utilisé pour identifier l’environnement fonctionnel associé au site.
3.3 Création actuelle d’un compte
Le flux actuel est le suivant :
1. L’utilisateur renseigne les informations administratives du compte.
2. L’utilisateur sélectionne l’équipe gestionnaire dans une liste unique.
3. L’utilisateur clique sur Suivant.
4. L’application affiche les sites disponibles.
5. L’utilisateur coche les sites sur lesquels le compte sera utilisé.
6. L’application crée les comptes correspondants dans l’Active Directory.
4. Besoin cible
Le besoin cible est de permettre à l’utilisateur de choisir explicitement les environnements pour lesquels un compte doit être créé, via des cases à cocher : TEST, RECETTE et PROD.
Pour chaque environnement sélectionné, l’application doit créer le compte AD suffixé correspondant et lui appliquer uniquement les équipes gestionnaires de l’environnement concerné.
Case cochée	Compte AD généré	Équipes gestionnaires appliquées
TEST	<nom>_test	Équipes TEST
RECETTE	<nom>_recette	Équipes RECETTE
PROD	<nom>_prod	Équipes PROD
Exemple : si l’utilisateur saisit le nom logique MONCOMPTE et coche TEST + RECETTE uniquement, les comptes AD créés seront MONCOMPTE_test et MONCOMPTE_recette. Aucun compte MONCOMPTE_prod ne sera créé.
5. Proposition d’évolution de l’IHM
L’IHM actuelle peut être conservée dans son principe général, afin de limiter l’impact utilisateur. L’évolution proposée est d’ajouter la sélection des environnements dans l’étape administrative, puis de filtrer les sites et les équipes selon les environnements cochés.
5.1 Étape 1 - Administratif
Ajouter un bloc obligatoire de sélection des environnements à créer.
Créer le compte pour :
[ ] TEST
[ ] RECETTE
[ ] PROD
Au moins un environnement doit être coché. En cas d’absence de sélection, le bouton Suivant doit être bloqué ou un message d’erreur doit être affiché.
5.2 Équipe gestionnaire
L’IHM actuelle contient une seule liste de sélection d’équipe gestionnaire. Dans le nouveau fonctionnement, cette liste ne doit plus être globale.
Proposition recommandée : ne pas demander à l’utilisateur de choisir manuellement une équipe différente pour chaque environnement. Les équipes gestionnaires seront déterminées automatiquement depuis la configuration de l’environnement au moment de la création des comptes suffixés.
Justification : cette approche évite à l’utilisateur de sélectionner par erreur une équipe TEST pour un compte PROD. Elle respecte mieux la règle métier : l’équipe gestionnaire est déduite de l’environnement du compte créé.
Si le besoin métier impose de laisser le choix à l’utilisateur, alors l’écran devra afficher une liste par environnement coché. Exemple : Équipe TEST, Équipe RECETTE, Équipe PROD. Cette option est plus lourde et nécessite davantage de contrôles IHM.
5.3 Étape 2 - Sites
L’écran actuel de sélection des sites est conservé, mais il devra être adapté afin de présenter uniquement les sites compatibles avec les environnements cochés à l’étape précédente.
L’utilisateur continuera à choisir les sites un par un, comme aujourd’hui. Chaque site affiché devra être associé à son environnement fonctionnel. Si plusieurs environnements sont cochés, la liste pourra être présentée groupée par environnement pour améliorer la lisibilité.
Exemple d’affichage cible :

TEST
[ ] Site T1   Nom du compte : MONCOMPTE_test
[ ] Site T2   Nom du compte : MONCOMPTE_test

RECETTE
[ ] Site R1   Nom du compte : MONCOMPTE_recette

PROD
[ ] Site P1   Nom du compte : MONCOMPTE_prod
[ ] Site P2   Nom du compte : MONCOMPTE_prod
5.4 Étape 3 - Confirmation
La page de confirmation devra afficher clairement les comptes AD qui seront créés, les environnements concernés, les sites sélectionnés et les équipes gestionnaires qui seront appliquées.
Compte logique : MONCOMPTE

Compte AD        Environnement   Sites sélectionnés   Équipes gestionnaires
MONCOMPTE_test   TEST            T1, T2               ADMIN_TEAMS_TEST
MONCOMPTE_prod   PROD            P1                   ADMIN_TEAMS_PROD
6. Évolution de la base de données
6.1 Table CONFIGURATION
La clé unique ADMIN_TEAMS doit être remplacée fonctionnellement par trois clés de configuration distinctes.
Clé	Description	Format
ADMIN_TEAMS_TEST	Équipes gestionnaires autorisées pour les comptes TEST	codes séparés par ';'
ADMIN_TEAMS_RECETTE	Équipes gestionnaires autorisées pour les comptes RECETTE	codes séparés par ';'
ADMIN_TEAMS_PROD	Équipes gestionnaires autorisées pour les comptes PROD	codes séparés par ';'
Exemple de script d’initialisation :

INSERT INTO CONFIGURATION (conf_key, conf_value)
VALUES ('ADMIN_TEAMS_TEST', '');

INSERT INTO CONFIGURATION (conf_key, conf_value)
VALUES ('ADMIN_TEAMS_RECETTE', '');

INSERT INTO CONFIGURATION (conf_key, conf_value)
VALUES ('ADMIN_TEAMS_PROD', '');
La clé ADMIN_TEAMS peut être conservée temporairement pour compatibilité technique, mais les nouveaux traitements ne devront plus s’appuyer dessus.
6.2 Table SITE
Aucune modification structurelle n’est prévue sur la table SITE. Le champ existant permettant de dissocier les sites sera utilisé pour rattacher un site à TEST, RECETTE ou PROD.
La correspondance exacte entre les valeurs techniques existantes et les libellés fonctionnels devra être confirmée dans le paramétrage de l’application.
Valeur technique site	Environnement fonctionnel
SIT	TEST
UAT	RECETTE
PRD	PROD
7. Nouveau flux de création de compte
1. L’utilisateur saisit les informations générales du compte logique.
2. L’utilisateur coche les environnements à créer : TEST, RECETTE, PROD.
3. L’utilisateur clique sur Suivant.
4. L’application charge les sites correspondant aux environnements cochés.
5. L’utilisateur sélectionne les sites un par un.
6. L’utilisateur accède à la page de confirmation.
7. Pour chaque environnement sélectionné et réellement utilisé par au moins un site :
   a. construction du nom du compte AD avec suffixe
   b. lecture des équipes gestionnaires de l’environnement
   c. contrôle de cohérence
   d. création ou mise à jour du compte AD
   e. affectation des équipes gestionnaires correspondantes
8. Affichage du résultat de création.
7.1 Règle de création des comptes suffixés
Environnement	Suffixe	Exemple pour COMPTE_TEST
TEST	_test	COMPTE_TEST_test
RECETTE	_recette	COMPTE_TEST_recette
PROD	_prod	COMPTE_TEST_prod
Un compte suffixé ne doit être créé que si l’environnement correspondant a été sélectionné par l’utilisateur et si au moins un site de cet environnement est retenu, sauf règle métier contraire.
8. Évolution des traitements back-end
8.1 Service de configuration
Créer ou faire évoluer un service permettant de récupérer les équipes gestionnaires selon l’environnement fonctionnel.
GetAdminTeams(environment)

Entrée : TEST / RECETTE / PROD
Sortie : liste des codes équipes autorisées

Mapping des clés :
TEST    -> ADMIN_TEAMS_TEST
RECETTE -> ADMIN_TEAMS_RECETTE
PROD    -> ADMIN_TEAMS_PROD
8.2 Service de sites
Le service de sites devra permettre de récupérer les sites par environnement afin d’alimenter l’étape de sélection des sites.
GetSitesByEnvironments(environments)

Entrée : liste des environnements cochés
Sortie : liste des sites compatibles, avec leur environnement fonctionnel
8.3 Service de création AD
Le service de création AD devra traiter les environnements sélectionnés séparément. Chaque compte suffixé est traité comme un compte AD distinct, avec ses propres équipes gestionnaires.
Pour chaque environnement sélectionné :

baseName = nom saisi par l’utilisateur
accountName = BuildAccountName(baseName, environment)
adminTeams = GetAdminTeams(environment)
selectedSites = GetSelectedSites(environment)

Validate(accountName, environment, adminTeams, selectedSites)
CreateOrUpdateAdAccount(accountName, adminTeams, selectedSites)
9. Flux de modification de compte
La modification doit appliquer les mêmes règles que la création. Lorsqu’un compte existant est modifié, l’application doit identifier le compte suffixé concerné et contrôler son environnement.
Exemples :
- modification de MONCOMPTE_test    -> équipes TEST uniquement
- modification de MONCOMPTE_recette -> équipes RECETTE uniquement
- modification de MONCOMPTE_prod    -> équipes PROD uniquement
Une modification ne doit pas permettre d’affecter à un compte suffixé des équipes gestionnaires provenant d’un autre environnement.
10. Contrôles métier
Code	Règle	Comportement attendu
RG01	Au moins un environnement doit être sélectionné.	Blocage avant passage à l’étape Sites.
RG02	Un site sélectionné doit appartenir à un environnement coché.	Site masqué ou sélection refusée.
RG03	Un compte suffixé doit recevoir uniquement les équipes de son environnement.	Blocage création/modification.
RG04	La clé de configuration de l’environnement doit exister.	Erreur technique explicite.
RG05	La liste des équipes ne doit pas être vide pour un environnement sélectionné.	Blocage avec message métier ou technique selon décision projet.
RG06	L’ancienne clé ADMIN_TEAMS ne doit plus être utilisée dans ce flux.	Contrôle technique / revue de code.
11. Messages d’erreur
Aucun environnement n’a été sélectionné.

Aucun site compatible n’est disponible pour les environnements sélectionnés.

L’équipe gestionnaire 3D60 n’est pas autorisée pour le compte MONCOMPTE_test.

La configuration ADMIN_TEAMS_RECETTE est absente ou vide.

Le site KJ appartient à l’environnement PROD et ne peut pas être associé au compte MONCOMPTE_test.
12. Administration de la configuration
L’écran de configuration de l’application doit permettre d’administrer les équipes gestionnaires par environnement. L’écran actuel listant les équipes gestionnaires devra évoluer pour afficher un critère environnement.
Affichage cible :

Environnement : [TEST / RECETTE / PROD]
Code équipe   : [____]

Liste :
Code équipe | Environnement | Actions
Les actions Ajouter, Modifier et Supprimer devront mettre à jour la clé CONFIGURATION correspondant à l’environnement sélectionné.
13. Reprise des données
Une reprise de données est nécessaire afin de répartir les équipes actuellement présentes dans ADMIN_TEAMS vers ADMIN_TEAMS_TEST, ADMIN_TEAMS_RECETTE et ADMIN_TEAMS_PROD.
La répartition doit être fournie ou validée par le métier, car elle ne peut pas être déduite automatiquement de manière fiable à partir de la configuration actuelle.
Étapes de reprise :

1. Extraire la valeur actuelle de ADMIN_TEAMS.
2. Obtenir la répartition métier des équipes par environnement.
3. Alimenter ADMIN_TEAMS_TEST.
4. Alimenter ADMIN_TEAMS_RECETTE.
5. Alimenter ADMIN_TEAMS_PROD.
6. Vérifier que les écrans et traitements n’utilisent plus ADMIN_TEAMS.
14. Cas de tests
Cas	Entrée	Action	Résultat attendu
CT01	TEST coché uniquement	Création compte	Création de <nom>_test uniquement.
CT02	RECETTE + PROD cochés	Création compte	Création de <nom>_recette et <nom>_prod.
CT03	Aucun environnement coché	Suivant	Blocage utilisateur.
CT04	Site PROD sélectionné pour compte TEST	Validation	Blocage métier.
CT05	ADMIN_TEAMS_TEST vide	Création TEST	Blocage ou erreur selon règle projet.
CT06	Modification de <nom>_recette	Changement équipes	Équipes RECETTE uniquement.
CT07	Ancienne clé ADMIN_TEAMS renseignée	Création	La clé n’est pas utilisée par le nouveau flux.
15. Points d’attention
Le nommage des comptes suffixés doit être centralisé dans une méthode unique afin d’éviter les incohérences entre création, modification et recherche.
Les contrôles doivent être implémentés côté serveur. Les filtrages IHM améliorent l’expérience utilisateur mais ne doivent pas être considérés comme une sécurité suffisante.
Les traitements existants qui lisent directement ADMIN_TEAMS devront être recensés et adaptés afin d’utiliser la nouvelle logique par environnement.
 

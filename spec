Description spécifications techniques
Après les échanges dans la réunion, nous avons compris que GMI utilise la DLL de PXE (PXE LIB) pour effectuer le remplacement ou la copie de poste.
Le problème réside dans la détermination du moment où la copie ou le remplacement est terminé afin de libérer la fiche. Pour ce faire, nous devons appeler le web service pour déflaguer le poste en tant que poste de référence.
Voici la procédure que nous allons suivre :
1-	Webservice PXE
a.	Un nouveau webservice pour flaguer une fiche comme poste de référence :
•	Avant le remplacement ou la copie d'un poste, il faut appeler ce webservice pour flaguer la fiche comme poste de référence afin de bloquer la suppression ou le remplacement d'un poste de référence
•	Route (Exemple)
o	https://webs-ni.cm-cic.fr/pxe/devbooster.asmx/flagAsReference?macaddress=E86A645CAD96&uuid=123E4567-E89B-12D3-A456-426614174001
	Paramètre : uuid et/ou macaddress
b.	Un nouveau webservice pour déflaguer une fiche comme poste de référence après la copie ou le remplacement 
•	Après la fin du remplacement ou le copie d’un poste, GMI doit absolument appeler ce webservice pour déflaguer la fiche dans PXE afin de le libérer 
•	Route (Exemple) :
o	https://webs-ni.cm-cic.fr/pxe/devbooster.asmx/unFlagAsReference?macaddress=E86A645CAD96&uuid=F1D0CF80-0BC4-11E9-9CB7-5073CC581000%C2%BB
	Paramètre : uuid et/ou macaddress 

c.	SUPRESSION : Blocage de la suppression de la fiche PXE si la fiche est flaguer comme poste de référence
•	Objectif : Empêcher la suppression de la fiche PXE si la fiche est flaguer comme poste de référence.
•	Action : Ajouter un contrôle dans PXE1 qui vérifie si une poste de référence. Si c'est le cas, bloquer la suppression de la fiche PXE et afficher un message d'erreur indiquant que la fiche ne peut pas être supprimée tant qu'elle est utilisée comme poste de référence.
o	https://webs-ni.cm-cic.fr/pxe/devbooster.asmx/{name}/delete
	Paramètre : name
2-	IHM
a-	On va afficher sur l’interface PXE si la fiche est un poste de référence
b-	Bloquer également la suppression au niveau de l'IHM si le poste est marqué comme fiche de référence 

3-	DLL pour faire le remplacement ou la copie (PXELIB)
a.	 Contrôle de pour un poste de référence en cours de remplacement
•	Objectif : Bloquer le remplacement d'un poste s'il est déjà en cours de remplacement
•	Action : Ajouter un contrôle dans PXE1 qui vérifie si le poste de référence est en cours de remplacement
o	Si c'est le cas, Bloquer le remplacement et afficher un message d'erreur indiquant que le poste ne peut pas être utilisé comme poste de référence tant qu'il est en cours de remplacement. 
b.	Contrôle de remplacement d'un poste saisi en tant que poste de référence comme model de copie 
•	Objectif : Bloquer le remplacement d'un poste s'il est saisi en tant que poste de référence pour modèle de copie.
•	Action : Ajouter un contrôle dans PXE1 qui vérifie si le poste à remplacer est utilisé comme poste de référence pour modèle de copie. 
o	Si c'est le cas, bloquer le remplacement et afficher un message d'erreur indiquant que le poste ne peut pas être remplacé tant qu'il est utilisé comme poste de référence. 

ne répond pas encore je vais te dire ce qu'on va faire après, juste pour te mettre dans le context


le client m'a posé cette question, repond pas encore mais y a encore autre information.

Mes questions :
- Au lieu d’avoir un top, est-ce que c’est possible d’avoir un compteur qu’on incrémente à la validation du GMI, et qu’on décimente à la validation de la tâche de personnalisation ? Ainsi si le compteur est >= 1 cela signifié qu’il est poste de référence
- Vous avez prévu de bloquer la suppression par IHM, mais il y a aussi la suppression demandé par GID ?

RQ : par rapport aux spécification :
- Côté GITG, nous faisons appel à PXE1_LIB
- Côté GMIS, GPL, PLANPROJ et EMMA , on passe par le webservice PXE de contrôle


et encore le client:
Je vous contact encore par rapport à la fiche de maintenance à valider concernant ce Rubis :

Vous parler uniquement de l’impact sur la DLL PXE1_LIB, mais pour le contrôle à la saisie nous appelons le Webservice PXESERVICESALLLISTES, est-ce que vous pensez aussi à adapter ce webservice pour nous remonter l’information sur le poste de référence ou le remplacement ?
o GMIS, GPL/PLANPROJ , EMMA : sont des outils de saisie de la mission pour l’installation ou le remplacement d’un poste :
Ils appellent le WEBSERVICE pour contrôler l’existence de poste de référence
o GITG est l’appli qui fait le chargement de la fiche PXE d’un poste ; c’est elle qui fait appel à la DLL PXE1_LIB pour le contrôle et le lancement du chargement

Le remplacement d’un poste :
Oralement, j’ai compris qu’il y aura deux tag un tag pour toper la fiche PXE comme poste de référence et un tag pour topé la fiche PXE comme en cours de remplacement.
Ceci n’est pas traduit dans la spécification : il y a un seul tag « Poste de référence ».
Or on a bien besoin de distinguer les deux :

Le cas d’un poste de référence : la fiche PXE peut être copier à plusieurs reprise ; la suppression et le remplacement n’est pas possible
Le cas d’un remplacement : la fiche PXE est remplacer ; c’est-à-dire elle est copié pour un nouveau poste ; puis supprimer
o A la saisie de la mission, on topera la fiche PXE comme en cours de remplacement ; Le poste de référence saisie pour le remplacement, ne peut plus être saisie en tant que poste de référence ailleurs
o A la fin du chargement, fin de remplacement, on tope le remplacement comme terminé
o Une fiche PXE remplacé ne peut plus service de fiche de référence mais peut être supprimée. Donc vous avez besoin de savoir que le remplacement est terminé pour autoriser la suppression.
ne repond pas encore , je te pose la question apres


je souhaite que tu me donne un autre spécification pour rebondir a ces remarque

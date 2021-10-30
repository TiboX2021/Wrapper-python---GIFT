"""
ATTENTION : POUR L'IMPORTATION DE FICHIERS :
AVANT DE CLIQUER SUR L'ONGLET "IMPORTER", SE PLACER DANS LA CATEGORIE DE BASE :
DEFAUT POUR PROJET EUCLIDE. Sinon, la catégorie de questions ne se crée pas dedans,
mais dans un dossier annexe, et les questions ne sont plus accessibles partout dans le projet Euclide
=> en fait, on doit se placer exactement dans le premier dossier mentionné dans le path, après "top/"

Génération de questions + ou - aléatoires pour les tests Moodle

Parameters.test_category

Utilisation :
-> création de groupes de questions + path
-> création d'un Parser
-> Parser.GiftData.append(groupe_questions)
-> Parser.write(destination=Parameters.banque + qqch)

path Moodle à ajouter: Parameters.test_category
"""



import pygift as pg


def numberToStr(number) -> str:
	"""Transforme les nombres du int python vers un str en français"""

	# 1er test : si le nombre est entier, on le convertit de int à float (423.0 -> 423)
	if int(number) == float(number):
		number = int(number)

	# Passage en chaîne de caractères
	string = str(number)

	i = string.find(".")

	# Remplacer '.' par ',' (syntaxe anglaise -> syntaxe française)
	if i != -1:
		string = string[:i] + "," + string[i+1:]
	
	return string


def randomNumber(numbers : int = 4) -> int:
	"""Génération de nombres aléatoires"""
	from random import randint
	return randint(10**(numbers-1), 10**numbers-1)


class MultiplicationAstucieuse:
	"""
	Catégorie de questions :
	multiplications / divisions par des nombres comme 1000, 0.001

	Règles de génération :
	- entre 1 et 3 zéros uniquement (il faudrait en faire autant de chaque. Objectif 400-500 questions?)
	1000, 100, 10, 0.1, 0.01, 0.001 : 6 nombres. On peut faire 10, 20, 30, 40 nombres aléat pour chaque multiplicateur

	- générer autant de multiplications que de divisions

	- choix du nombre à modifier:

	On prend un nombre à 4 chiffres, qu'on divise par 1 jusqu'à 10**6 pour obtenir un éventail large:
	de 10**0 à 10*6 : 7 valeurs différentes.

	On a 6 valeurs : [1000, 100, 10, 0.1, 0.01, 0.001], et * ou / ce qui fait 12 possibilités

	au total : nombre de questions : n = 12 * 7 * nombres générés par diviseurs

	= 84 * i. On peut prendre i = 3 ou 4 pour avoir un nombre conséquent de questions : n = 4 paraît pas mal
	"""

	repetitions = 4
	diviseurs = [10**i for i in range(0, 7)]  # Déplacement de la virgule

	facteurs = [1000, 100, 10, 0.1, 0.01, 0.001]

	@staticmethod
	def banque_nombres(reps : int = repetitions) -> list[float]:
		"""
		Génération aléatoire de nombres de 1 à 4 chiffres, dont on peut ensuite déplacer la
		virgule de 0 à 6 fois pour randomiser. Génère un banque de nombres à utiliser pour
		générer les questions	
		"""
		liste = []

		for diviseur in MultiplicationAstucieuse.diviseurs:  # 7 diviseurs différents, de 1 à 10**6

			for rep in range(reps):

				liste.append(randomNumber()/diviseur)

		return liste

	@staticmethod	
	def generer() -> list[pg.Question]:
		"""
		Format de l'opération :
		nombre */ facteur = resultat

		On utilise * puis /
		Pour avoir un code plus propre, via une fonction qui prend un
		opérateur en argument

		Pour l'instant, aucun feedback
		"""

		titre = "Multiplication & division astucieuse"
		arrondi = 10  # Problème d'arrondi numérique : ça peut aller jusqu'à division par 10**9 : 10è chiffre

		# Banque de nombres à utiliser
		nombres = MultiplicationAstucieuse.banque_nombres()

		# Liste de questions à remplir
		liste_questions = []

		# Création de chaque question
		for facteur in MultiplicationAstucieuse.facteurs:
			for nombre in nombres:

				# 1ère opération : multiplication
				resultat = round(nombre * facteur, arrondi)

				bonne_reponse = pg.Answer(percent="100", answer=numberToStr(resultat), feedback="")

				# Réponse par défaut : à voir, si nécessaire
				# mauvaise_reponse = pg.ShortAnswerQuestion.defaultAnswer(feedback="feedback mauvaise reponse")

				question = pg.ShortAnswerQuestion(id=0, title=titre,
					text=f"{numberToStr(nombre)} x {numberToStr(facteur)}",
					answers=[bonne_reponse])

				# Ajout de la question :
				liste_questions.append(question)


				# 2ème opération : division
				resultat = round(nombre / facteur, arrondi)

				bonne_reponse = pg.Answer(percent="100", answer=numberToStr(resultat), feedback=None)

				# Réponse par défaut : à voir, si nécessaire
				# mauvaise_reponse = pg.ShortAnswerQuestion.defaultAnswer(feedback="feedback mauvaise reponse")

				question = pg.ShortAnswerQuestion(id=0, title=titre,
					text=f"{numberToStr(nombre)} / {numberToStr(facteur)}",
					answers=[bonne_reponse])

				# Ajout de la question :
				liste_questions.append(question)
		
		return liste_questions



# Nouvelle catégorie de questions
# TODO : à beaucoup simplifier
class MultiplicationDecimale:
	"""
	Multiplications entre deux nombres, dont l'un décimal ou rond
	Objectif : faire des tables de multiplication, mais avec des virgules, dizaines, ou centaines

	Génération : 
	-> liste 1 : de 2 à 9
	-> liste 2 : de 2 à 9 après avoir été divisés par 10, multipliés par 10 ou 100

	Nombre total de combinaisons : 9 x 9 x 3 = 243
	"""
	tables = [k for k in range(2, 10)]

	@staticmethod
	def banque_nombres() -> list[float]:

		return [k for i in MultiplicationDecimale.tables for k in (i / 10, i * 10, i * 100)]

	@staticmethod
	def generer() -> list[pg.Question]:

		titre = "Multiplication décimale"

		liste1 = MultiplicationDecimale.tables
		liste2 = MultiplicationDecimale.banque_nombres()

		questions = []

		for n1 in liste1:
			for n2 in liste2:

				# Création de la question
				resultat = round(n1 * n2, 4)  # Problème d'arrondi : ça descendra jamais plus loin que 10**-4

				bonne_reponse = pg.Answer(percent="100", answer=numberToStr(resultat), feedback=None)

				question = pg.ShortAnswerQuestion(id=0, title=titre,
					text=f"{numberToStr(n1)} x {numberToStr(n2)}",
					answers=[bonne_reponse])

				questions.append(question)

		return questions


class AdditionAstucieuse:
	"""
	Addition de 4 nombres entiers qui tombe juste sur des nombres ronds.
	On peut ajouter un 5ième nombre aléatoire "intrus" pour complexifier la chose

	Génération :
	Générer un nombre et son complémentaire pour obtenir un nombre rond
	(on répète cette étape 2 fois pour obtenir un nombre rond)
	-> générer un nombre aléatoire entre 1 et 40
	-> générer un nombre rond comme objectif:
	* générer un nombre aléatoire entre 5 et 10
	* multiplier par 10
	-> calculer le compémentaire à partir du nombre de départ et d'arrivée
	"""

	@staticmethod
	def nombreEtComplementaire() -> tuple[int, int]:
		from random import randint
		nombre1 = randint(1, 40)

		objectif = randint(5, 10) * 10

		nombre2 = objectif - nombre1

		return (nombre1, nombre2)


	@staticmethod
	def banque_nombres(n : int, paires : int = 2, intrus : bool = False) -> list[list[int]]:
		"""
		Génère n listes de nombres pour la création de questions
		"""
		from random import randint, shuffle
		liste_questions = []

		for i in range(n):

			liste_question = []

			for j in range(paires):
				n1, n2 = AdditionAstucieuse.nombreEtComplementaire()
				liste_question.append(n1)
				liste_question.append(n2)

			if intrus:  # Ajout d'un nombre supplémentaire si nécessaire
				liste_question.append(randint(1, 40))

			# Changement de l'ordre des nombres aléatoirement
			shuffle(liste_question)

			liste_questions.append(liste_question)

		return liste_questions


	@staticmethod
	def generer(n : int = 100, paires : int = 2, intrus : bool = False) -> list[pg.Question]:

		combinaisons = AdditionAstucieuse.banque_nombres(n, paires, intrus)

		titre = f"Addition astucieuse {'niveau 0' if intrus else 'niveau 1'}" # Niveau 2 si intrus et 2 paires

		questions = []

		def question_text(numbers : list[int]) -> str:

			text = numberToStr(numbers[0])

			for i in range(1, len(numbers)):

				text += f" + {numberToStr(numbers[i])}"

			return text

		for combinaison in combinaisons:

			# Bonne réponse : via la somme de tous les nombres
			bonne_reponse = pg.Answer(percent="100", answer=numberToStr(sum(combinaison)), feedback=None)

			question = pg.ShortAnswerQuestion(id=0, title=titre,
				text=question_text(combinaison),
				answers=[bonne_reponse])

			questions.append(question)

		return questions


class ConversionNqKm:
	"""
	Conversion de nautique vers kilomètre et inversement
	Pas la peine de mélanger les questions, vu qu'on le fait via "questions aléatoires"
	Niveau 1 : nombres ronds
	Niveau 2 : nombres ronds qui donnent des nombres à virgule

	Nq -> Km : x 2 puis -10%

	Pour générer ça, 
	ex : 25, 50, 100 nq -> un truc qui donne un nombre rond quand on fait x2
	on peut prendre toutes les dizaines et trucs qui finissent par 5
	-> ça fait 20 questions
	Idem : tomber sur 190 quand on fait x2, puis faire -10%, c'est pas évident.

	Km -> Nq : /2 puis + 10%

	Pour générer ça,
	On prend tous les nombres de 10 à 200 puis on fait * 2, pour que la division par 2 tombe sur des nombres ronds
	après, faire 380 /2 -> 190 puis +10% -> 201, c'est peut être un peu difficile, PAS GRAVE
	ATTENTION : COMME C'EST APPROXIMATIF, les 2 méthodes ne se compensent pas. Il faut trouver d'autres nombres

	20 questions de chaque -> 40 questions en tout, pas mal
	"""

	def generer() -> list[pg.Question]:

		liste_questions = []

		# Listes de nombres
		nqToKm = list(range(5, 105, 5))
		kmToNq = list(range(20, 400, 20))

		titre = "Conversion nautique - kilomètre"

		# Génération des questions
		for conversion in nqToKm:

			resultat = round(conversion * 2 * 0.9, 3)  # Round pour éviter les approximations à 0.9999999



			# Création des réponses possibles
			bonne_reponse = pg.Answer(percent="100", answer=numberToStr(resultat), feedback=None)

			feedback_erreur = (
				"Conversion de nautiques en kilomètres : multiplier par 2, puis enlever 10%. "
				"Pour obtenir les 10% à soustraire, il suffit de multiplier le nombre par 10/100, "
				"ce qui revient à le divier par 10"
			)
			mauvaise_reponse = pg.ShortAnswerQuestion.defaultAnswer(feedback_erreur)

			# Création de la question
			question = pg.ShortAnswerQuestion(id=0, title=titre,
				text=f"Convertir {conversion} nautiques (nq) en kilomètres (km)",
				answers=[bonne_reponse, mauvaise_reponse])

			# Ajout de la question :
			liste_questions.append(question)

		# Idem pour la conversion dans l'autre sens
		for conversion in nqToKm:

			resultat = round(conversion / 2 * 1.1, 3)  # Round pour éviter les approximations à 0.9999999



			# Création des réponses possibles
			bonne_reponse = pg.Answer(percent="100", answer=numberToStr(resultat), feedback="")

			feedback_erreur = (
				"Conversion de kilomètres en nautiques : diviser par 2, puis ajouter 10%. "
				"Pour obtenir les 10% à ajouter, il suffit de multiplier le nombre par 10/100, "
				"ce qui revient à le divier par 10"
			)
			mauvaise_reponse = pg.ShortAnswerQuestion.defaultAnswer(feedback_erreur)

			# Création de la question
			question = pg.ShortAnswerQuestion(id=0, title=titre,
				text=f"Convertir {conversion} kilomètres (km) en nautiques (nq)",
				answers=[bonne_reponse, mauvaise_reponse])

			# Ajout de la question :
			liste_questions.append(question)

		return liste_questions



if __name__ == "__main__":

	
	# Création de la banque de questions
	groupe = pg.QuestionGroup()

	filename = "Conversions km - nautiques.txt"

	groupe.path = pg.Path(pg.Parameters.test_category + filename)

	groupe.questions = ConversionNqKm.generer()

	parser = pg.Parser()

	parser.addQuestionGroup(groupe)

	parser.write(filepath=pg.Parameters.banque_test + filename)

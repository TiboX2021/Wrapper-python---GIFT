"""
FAIT AVEC PYTHON 3.10 (nécessaire pour list[str])

ATTENTION :
dans les textes, éviter d'utiliser des caractères spéciaux du style \, :, $, #, qui servent à délimiter le texte

REMARQUE:
en utilisant parser.cleanHTMLText, on rajoute des <br> qui n'étaient pas là dans les feedback spécifiques des
questions VRAI FAUX. A suivre, ça pourrait être gênant et justifier un léger changement. Idem pour le texte.
Après upload, on dirait que ça change rien
"""
from typing import Type
import parser as p


class Parameters:

	# Paramètres
	default_category = "top/Défaut pour Projet EUCLIDE/"  # ATTENTION
	test_category = "top/Défaut pour Projet EUCLIDE/Idées de questions/"
	downloads = "C:\\Users\\Thibaut de Saivre\\Downloads\\"
	banque = "C:\\Users\\Thibaut de Saivre\\Desktop\\Projet stage CIN\\Banque de question\\"
	banque_test = "C:\\Users\\Thibaut de Saivre\\Desktop\\Projet stage CIN\\Banque de question\\Idées de questions\\"

	# Si un bloc commence par ça, c'est un chemin de dossier. Sinon, c'est une question
	path_identifier = "// question: 0"
	category_identifier = "$CATEGORY:"
	
	# Identificateurs des paramètres de la question
	id_prefix, id_suffix = "question: ", "  name"
	name_prefix, name_suffix = "name: ", "\n"
	text_prefix, text_suffix = "<p>", "</p>"

	# Idem pour path
	path_prefix, path_suffix = "Switch category to ", "\n"

	# Pour indenter les blocs de données (lisibilité)
	indent = '\t'  # tabulation


## CLASSES CONTENEURS DE DONNEES

class Path:
	"""
	Stocke le dossier Moodle correspondant au set de questions
	toString : convertir l'objet Path en str au format GIFT
	fromString : convertir un str au format GIFT en objet Path
	PRESUPPOSE : ON SE SITUE DEJA DANS LE DOSSIER COURS

	// question: 0  name: Switch category to $course$/top/Défaut pour Test Thibaut
	$CATEGORY: $course$/top/Défaut pour Test Thibaut
	"""
	def __init__(self, path : str) -> None:

		self.path = path

	def toString(self) -> str:

		return (
			f"{Parameters.path_identifier}  name: Switch category to {self.path}\n"
			f"{Parameters.category_identifier} {self.path}"
		)

	@classmethod
	def fromString(cls, string : str):
		
		return cls(path=p.parseArgument(string, Parameters.path_prefix, Parameters.path_suffix))


class Answer:
	"""
	Permet de stocker le %age de points, la réponse correspondante, et plein d'autres choses
	"""
	def __init__(self, percent : str, answer : str, feedback : str) -> None:
		self.percent = percent
		self.answer = answer
		self.feedback = feedback

	def toString(self) -> str:
		"""
		Renvoie la ligne qui correspond à une réponse possible, sans le préfixe = ou ~.
		format:
		%100%réponse correcte 1 (note de 100%)#<p>feedback spécifique pour la réponse 1<br></p>
		"""
		return f"%{self.percent}%{self.answer}#{p.feedbackTextFormat(self.feedback) if self.feedback is not None else ''}"

	@classmethod
	def fromString(cls, string : str):
		
		percent = p.parseArgument(string, prefix='%', suffix='%')

		# Il faut éliminer les 2 premiers %, qui sont : %pourcentage%texteRéponse
		answer_text = p.parseArgument(string[2:], prefix='%', suffix='#')

		# Feedback s'il existe
		answer_feedback = string.split('#')[1]
		if answer_feedback == "":
			answer_feedback = None
		else:
			answer_feedback = p.cleanHTMLText(answer_feedback)

		# création d'une réponse
		return cls(percent=percent, answer=answer_text, feedback=answer_feedback)


class Question:
	"""
	Classe de base qui contient les métadonnées
	"""
	def __init__(self, id : int=0, title : str="", text : str="") -> None:
		
		self.id = id
		self.title = title
		self.text = text

		self.general_feedback = None  # A moins qu'il ne soit défini plus tard

	@staticmethod
	def parseMetadata(metadata : str) -> tuple[int, str, str]:
		"""
		Récupération des métadonnées
		"""
		return (
			int(p.parseArgument(metadata, Parameters.id_prefix, Parameters.id_suffix)),
			p.parseArgument(metadata, Parameters.name_prefix, Parameters.name_suffix),
			p.cleanHTMLText(p.parseArgument(metadata, Parameters.text_prefix, Parameters.text_suffix))  # enlever <br>
		)


	def metadataToString(self) -> str:
		"""
		Renvoie les métadonnées de la question sous forme de str au format GIFT:
		// question: 31354  name: question test feedback
		::question test feedback::[html]<p>ceci est le texte de la question<br></p>
		"""
		return (
			f"// question: {self.id}  name: {self.title}\n"
			f"::{self.title}::[html]{p.feedbackTextFormat(self.text)}"
		)


	def toString(self) -> str:
		"""
		Méthode 'virtuelle', à redéfinir dans les autres classes
		"""
		return ""

	@classmethod
	def fromString(cls, string : str):
		"""
		Méthode "virtuelle"
		"""
		return None  # De toutes façons, cette méthode n'est jamais sensée être appelée


class QuestionGroup:
	"""
	Contient un chemin de dossier et une liste de questions. Simple conteneur
	"""
	path : Path
	questions : list[Question]
	
	def __init__(self) -> None:

		self.path = None
		self.questions : list[Answer] = []

	def isEmpty(self) -> bool:
		return self.questions == []

	def toString(self) -> str:
		"""
		Renvoie la représentation str au format GIFT de tout le bloc
		"""
		
		string = ""

		# Ajout du path
		if self.path is not None:
			string = self.path.toString()

		# Ajout des questions
		for question in self.questions:

			string += f"\n\n\n{question.toString()}"

		if self.path is None:
			return string[3:]  # On retire les 3 1ers retours à la ligne superflus
		else:
			return string


## CLASSES DE QUESTIONS PRECISES	

class ShortAnswerQuestion(Question):

	def __init__(self, id: int=0, title: str="", text: str="", answers : list[Answer]=None, general_feedback : str=None) -> None:
		super().__init__(id, title, text)

		self.answers = answers
		self.general_feedback = general_feedback


	def toString(self) -> str:
		"""
		Renvoie une chaîne de caractères qui correspond à cette question au format GIFT
		"""
		# Données :
		data = "{\n"

		# Ajout des différentes réponses
		for answer in self.answers:
			data += f"{Parameters.indent}={answer.toString()}\n"  # Ajout de la ligne + retour à la ligne

		# Ajout du feedback général s'il est défini
		if self.general_feedback is not None:
			data += f"{Parameters.indent}####{p.feedbackTextFormat(self.general_feedback)}\n"

		# Cloture du bloc de données
		data += "}"

		return self.metadataToString() + data


	@classmethod
	def fromString(cls, string: str):

		new_instance = cls()
		# Séparation des données en métadonnées + données
		metadata = string.split('{')[0]
		data = p.parseArgument(string, prefix='{', suffix='}')

		# Métadonnées
		question_id, title, text = Question.parseMetadata(metadata)  # A donner en arg à la classe Question

		new_instance.id = question_id
		new_instance.title = title
		new_instance.text = text

		# Données
		# Lecture du bloc de données ligne par ligne
		lines = p.splitLines(data)
		lines = p.removeEmptyLines(lines)

		answers : list[Answer] = []  # Réponses possibles
		general_feedback = None

		for line in lines:

			line = p.removeIndent(line)
			first_char = line[0]

			if first_char == '=':

				# création d'une réponse
				answers.append(Answer.fromString(line[1:]))  # [1:] pour éliminer "="
			
			elif first_char == '#':
				general_feedback = p.cleanHTMLText(line.split("####")[1])

		# On initialise les derniers membres
		new_instance.answers = answers
		new_instance.general_feedback = general_feedback

		return new_instance

	@staticmethod
	def defaultAnswer(feedback : str):

		return Answer(percent="0", answer="*", feedback=feedback)
	

class TrueFalseQuestion(Question):
	"""
	// question: 31356  name: question vrai faux
	::question vrai faux::[html]<p>texte question vrai faux</p>{FALSE#<p>feedback vrai (mauvaise reponse)</p>#<p>feedback faux (bonne reponse)</p>}
	"""
	def __init__(self, id: int = 0, title: str = "", text: str = "", right_answer : bool = None, right_feedback : str = "", wrong_feedback : str = "") -> None:
		super().__init__(id=id, title=title, text=text)

		self.right_answer = right_answer
		self.right_feedback = right_feedback
		self.wrong_feedback = wrong_feedback

	
	def toString(self) -> str:
		# Données :
		data = "{"

		# Ajout de la réponse correcte
		data += ("TRUE" if self.right_answer == True else "FALSE")

		# Ajout du feedback de la mauvaise réponse
		data += f"#{p.feedbackTextFormat(self.wrong_feedback) if self.wrong_feedback != '' else ''}" 
		
		# Ajout du feedback de la bonne réponse
		data += f"#{p.feedbackTextFormat(self.right_feedback) if self.right_feedback != '' else ''}" 

		# Ajout du feedback général (uniquement s'il est défini)
		if self.general_feedback is not None:
			data += f"####{p.feedbackTextFormat(self.general_feedback)}"

		# Cloture du bloc de données
		data += "}"

		return self.metadataToString() + data

	@classmethod
	def fromString(cls, string : str):

		new_instance = cls()
		# Séparation des données en métadonnées + données
		metadata = string.split('{')[0]
		data = p.parseArgument(string, prefix='{', suffix='}')

		# Métadonnées
		question_id, title, text = Question.parseMetadata(metadata)  # A donner en arg à la classe Question

		new_instance.id = question_id
		new_instance.title = title
		new_instance.text = text

		# Données		
		# Récupération de la bonne réponse (une comparaison bête suffit)
		new_instance.right_answer = (data[:4] == "TRUE")

		# Récupération du mauvais feedback (qui est coincé entre les 2 #, facile à récupérer)
		new_instance.wrong_feedback = p.cleanHTMLText(p.parseArgument(data, prefix="#", suffix="#"))

		# Récupération du bon feedback : +2 pour skip le 1er et 2ème #. Pour la fin, début du #### ou jusqu'au bout
		new_instance.right_feedback = p.cleanHTMLText(data[data.find(
			f"#{new_instance.wrong_feedback}") + 2 + len(new_instance.wrong_feedback):
			i if (i := data.find("####")) != -1 else len(data)])

		# Récupération du feedback général
		if (i := data.find("####")) != -1:
			new_instance.general_feedback = p.cleanHTMLText(data[i + 4:])  #jusqu'au bout

		return new_instance


class QCM(Question):
	"""
	Remarque : la somme des bonnes réponses doit pouvoir donner 100% des points
	"""

	def __init__(self, id: int=0, title: str="", text: str="", answers : list[Answer]=None, general_feedback : str=None) -> None:
		super().__init__(id, title, text)

		self.answers = answers
		self.general_feedback = general_feedback


	def toString(self) -> str:
		"""
		Renvoie une chaîne de caractères qui correspond à cette question au format GIFT
		"""
		# Données :
		data = "{\n"

		# Ajout des différentes réponses
		for answer in self.answers:
			data += f"{Parameters.indent}~{answer.toString()}\n"  # Ajout de la ligne + retour à la ligne

		# Ajout du feedback général s'il est défini
		if self.general_feedback is not None:
			data += f"{Parameters.indent}####{p.feedbackTextFormat(self.general_feedback)}\n"

		# Cloture du bloc de données
		data += "}"

		return self.metadataToString() + data


	@classmethod
	def fromString(cls, string: str):

		new_instance = cls()
		# Séparation des données en métadonnées + données
		metadata = string.split('{')[0]
		data = p.parseArgument(string, prefix='{', suffix='}')

		# Métadonnées
		question_id, title, text = Question.parseMetadata(metadata)  # A donner en arg à la classe Question

		new_instance.id = question_id
		new_instance.title = title
		new_instance.text = text

		# Données
		# Lecture du bloc de données ligne par ligne
		lines = p.splitLines(data)
		lines = p.removeEmptyLines(lines)

		answers : list[Answer] = []  # Réponses possibles
		general_feedback = None

		for line in lines:

			line = p.removeIndent(line)
			first_char = line[0]

			if first_char == '~':

				# création d'une réponse
				answers.append(Answer.fromString(line[1:]))  # [1:] pour éliminer "="
			
			elif first_char == '#':
				general_feedback = p.cleanHTMLText(line.split("####")[1])

		# On initialise les derniers membres
		new_instance.answers = answers
		new_instance.general_feedback = general_feedback

		return new_instance


## Parser : intermédiaire entre les objets python et le fichier .txt au format GIFT

class Parser:
	"""
	Prend en argument un fichier, et est capable de le lire et d'écrire dedans au format GIFT
	"""
	def __init__(self, filepath : str = "") -> None:
		
		self.filepath = filepath
		self.GiftData : list[QuestionGroup]= []

	
	def addQuestionGroup(self, group : QuestionGroup):
		"""
		Ajoute un groupe de question aux données SEULEMENT S'IL EST NON VIDE
		"""
		if not group.isEmpty():
			self.GiftData.append(group)
			print("Groupe de questions ajouté")


	def parse(self):

		print(f"Lecture des données du fichier : {self.filepath}")
		# Lecture des données du fichier
		file = open(self.filepath, encoding="utf-8")
		blocks = p.splitBlocks(file.readlines())
		file.close()

		# Données à remplir
		group = QuestionGroup()

		for block in blocks:

			# Analyse de chaque bloc
			if Parser.isPath(block):  # Le bloc définit un chemin de dossier

				print("\nNouveau dossier")

				# Ajout du groupe précédent à la liste s'il n'est pas vide
				self.addQuestionGroup(group)

				# Création d'un nouveau groupe
				group = QuestionGroup()  # Reset du groupe de questions
				group.path = Path.fromString(block) # Lecture du path
				
			else:  # Le bloc représente une question : identifier le bon type de question

				# Analyse du type de question, puis traitement
				data = p.parseArgument(block, prefix='{', suffix='}')

				# Identification du type de question à l'aide du premier caractère des données
				first_char = p.firstChar(data)
				
				if first_char == '=':
					group.questions.append(ShortAnswerQuestion.fromString(block))
				elif first_char == '~':
					group.questions.append(QCM.fromString(block))
				else:
					group.questions.append(TrueFalseQuestion.fromString(block))

		# Ajout du dernier groupe :
		self.addQuestionGroup(group)

	
	def write(self, filepath : str = None):
		"""
		Réécrit les données dans le fichier spécifié (ou le fichier d'origine sinon)
		Ecrase les données précédentes !
		"""
		if filepath is None:
			filepath = self.filepath

		file = open(filepath, "w", encoding="utf-8")

		for group in self.GiftData:
			file.write(group.toString())
		file .close()


	# Méthodes utiles:
	@staticmethod
	def isPath(block : str) -> bool:
		return block.startswith(Parameters.path_identifier)


# test
# pour que ça marche : run python file in terminal
if __name__ == "__main__":

	filename = "add2.txt"

	destination = "C:\\Users\\Thibaut de Saivre\\Desktop\\Projet stage CIN\\Banque de question\\Opérations entières\\"

	category = Parameters.default_category + "Opérations entières/Additions 2"

	parser = Parser(filepath=Parameters.downloads + filename)

	parser.parse()

	parser.GiftData[0].path.path = category

	parser.write(destination + "Additions 2.txt")
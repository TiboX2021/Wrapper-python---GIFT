def parseArgument(string : str, prefix : str, suffix : str) -> str:
	"""
	S'il y a "xxxxx name: nom xxxxx", parseArgument(string, "name:") renvoie "nom"
	"""
	start_index = string.find(prefix) + len(prefix)
	end_index = string[start_index:].find(suffix)
	start_index

	return string[start_index: start_index + end_index]


def firstChar(string : str) -> str:
	"""
	Données en "{    =qqch}"
	Renvoie le 1er caractère qui n'est pas ' ' ou \n
	Sinon renvoie ""
	"""
	for char in string:
		if char != ' ' and char != '\n' and char != '\t':
			return char
	return ' '  # Par défaut


def splitBlocks(lines : list[str]) -> list[str]:
	"""
	Renvoie la liste des blocs de textes contenus dans la variable "texte"
	"""
	blocks = []

	block = ""

	for line in lines:

		if line != "\n":  # ligne vide : finit par un caractère retour à la ligne

			block += f"{line}"
		
		elif block != "":

			blocks.append(block)
			block = ""
	
	return blocks


def splitLines(block : str) -> list[str]:
	"""
	Sépare un paragraphe en liste de lignes
	"""
	return block.split('\n')


def cleanHTMLText(text : str) -> str:
	"""
	Enlève les balises <br>, <p>, </p> du texte
	(vu que dans les feedback, parfois il y en a, parfois non)
	Attention : si on veut mettre des inégalités, ça peut être compliqué
	"""


	return text.replace("<br>", "").replace("<p>", "").replace("</p>", "")


def feedbackTextFormat(text : str) -> str:
	"""
	Rajoute les balises p et br
	<p>texte du feedback<br></p>
	"""
	return f"<p>{text}<br></p>"


def removeIndent(line : str) -> str:
	"""
	Retire les tabulations / espaces au début de la ligne
	"""
	first_char_index = 0
	while first_char_index < len(line) and (line[first_char_index] == "\t" or line[first_char_index]  == " "):

		first_char_index += 1
	
	return line[first_char_index:]


def removeEmptyLines(lines : list[str]) -> list[str]:
	"""
	Enlève les lignes vides
	"""
	new_lines = []

	for line in lines:

		if line != "":
			new_lines.append(line)

	return new_lines

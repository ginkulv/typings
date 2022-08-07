import sys
import ctypes
import random

from enum import Enum
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

english_words = ["a", "about", "all", "also", "and", "as", "at", "be", "because", "but", "by", "can", "come", "could", "day", "do", "even", "find", "first", "for", "from", "get", "give", "go", "have", "he", "her", "here", "him", "his", "how", "I", "if", "in", "into", "it", "its", "just", "know", "like", "look", "make", "man", "many", "me", "more", "my", "new", "no", "not", "now", "of", "on", "one", "only", "or", "other", "our", "out", "people", "say", "see", "she", "so", "some", "take", "tell", "than", "that", "the", "their", "them", "then", "there", "these", "they", "thing", "think", "this", "those", "time", "to", "two", "up", "use", "very", "want", "way", "we", "well", "what", "when", "which", "who", "will", "with", "would", "year", "you", "your"]
russian_words = [ "и", "в", "не", "он", "на", "я", "что", "тот", "быть", "с", "а", "весь", "это", "как", "она", "по", "но", "они", "к", "у", "ты", "из", "мы", "за", "вы", "так", "же", "от", "сказать", "этот", "который", "мочь", "человек", "о", "один", "еще", "бы", "такой", "только", "себя", "свое", "какой", "когда", "уже", "для", "вот", "кто", "да", "говорить", "год", "знать", "мой", "до", "или", "если", "время", "рука", "нет", "самый", "ни", "стать", "большой", "даже", "другой", "наш", "свой", "ну", "под", "где", "дело", "есть", "сам", "раз", "чтобы", "два", "там", "чем", "глаз", "жизнь", "первый", "день", "тута", "во", "ничто", "потом", "очень", "со", "хотеть", "ли", "при", "голова", "надо", "без", "видеть", "идти", "теперь", "тоже", "стоять", "друг", "дом", "сейчас", "можно", "после", "слово", "здесь", "думать", "место", "спросить", "через", "лицо", "что", "тогда", "ведь", "хороший", "каждый", "новый", "жить", "должный", "смотреть", "почему", "потому", "сторона", "просто", "нога", "сидеть", "понять", "иметь", "конечный", "делать", "вдруг", "над", "взять", "никто", "сделать", "дверь", "перед", "нужный", "понимать", "казаться", "работа", "три", "ваш", "уж", "земля", "конец", "несколько", "час", "голос", "город", "последний", "пока", "хорошо", "давать", "вода", "более", "хотя", "всегда", "второй", "куда", "пойти", "стол", "ребенок", "увидеть", "сила", "отец", "женщина", "машина", "случай", "ночь", "сразу", "мир", "совсем", "остаться", "об", "вид", "выйти", "дать", "работать", "любить", "старый", "почти", "ряд", "оказаться", "начало", "твой", "вопрос", "много", "война", "снова", "ответить", "между", "подумать", "опять", "белый", "деньги", "значить", "про", "лишь", "минута", "жена", "посмотреть", "правда", "главный", "страна", "свет", "ждать", "мать", "будто", "никогда", "товарищ", "дорога", "однако", "лежать", "именно", "окно", "никакой", "найти", "писать", "комната", "москва", "часть", "вообще", "книга", "маленький", "улица", "решить", "далекий", "душа", "чуть", "вернуться", "утро", "некоторый", "считать", "сколько", "помнить", "вечер", "пол", "таки", "получить", "народ", "плечо", "хоть", "сегодня", "бог", "вместе", "взгляд", "ходить", "зачем", "советский", "русский", "бывать", "полный", "прийти", "палец", "россия", "любой", "история", "наконец", "мысль", "узнать", "назад", "общий", "заметить", "словно"]

class Highlight(Enum):
	NORMAL = 0
	RIGHT = 1
	WRONG = 2
	UPCOMING = 3

class Word(object):
	text: str = ''
	highlight: Highlight = Highlight.NORMAL
	colors = {
		Highlight.NORMAL: "#000000",
		Highlight.RIGHT: "#7CFC00",
		Highlight.WRONG: "#FF00FF",
		Highlight.UPCOMING: "#89CFF0"
	}

	def __init__(self, text):
		self.text = text
		self.highlight = Highlight.NORMAL

	def __str__(self):
		return f'<b style="color: {self.colors[self.highlight]};">{self.text}</b>'
		
def getLayout() -> str:
	layout = ctypes.windll.user32.GetKeyboardLayout(0)
	# 67699721 -> en
	# 68748313 -> ru
	if layout == 67699721:
		return 'en'
	return 'ru'

class Window(QMainWindow):
	current_index: int = 0
	current_words: list[Word] = []
	sample_size: int = 100

	def __init__(self, width: int, height: int):
		super().__init__()

		# Set up words
		window_width, window_height = int(width * 0.6), 400
		self.current_words = self.getWords(self.sample_size)

		# Set up window
		self.setWindowOpacity(0.9)
		self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
		self.setGeometry(int(width * 0.2), int(height * 0.6), window_width, window_height)
		self.setStyleSheet('background-color: #808080')

		# Set up label for words
		self.label = QLabel(self.prepareText(self.current_words, 0, Highlight.UPCOMING), self)
		# self.label = QLabel('word <b style="color: #0000FF;">word</b>', self)
		self.label.setFont(QFont('Hack NF'))
		self.label.move(150, 200)
		self.label.setGeometry(int(window_width * 0.05), int(window_height * 0.1), int(window_width * 0.9), int(window_height * 0.2))
		self.label.setWordWrap(True)
		self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.label.setStyleSheet('color: black; font-size: 28px; border: 1px solid black;')

		# Set up textbox
		self.textbox = QLineEdit(self)
		self.textbox.setGeometry(0, 0, int(window_width * 0.4), 40)
		self.textbox.move(int(window_width * 0.3), window_height - 60)
		self.textbox.textChanged.connect(self.processInput)
		self.textbox.installEventFilter(self)
		self.textbox.setFont(QFont('Hack NF'))
		self.textbox.setStyleSheet('border: 2px solid #006080; background-color: white; font-size: 20px')

		self.show()

	def keyPressEvent(self, event):
		# Exit on Escape
		if event.key() == Qt.Key.Key_Escape:
			sys.exit()
		# Reset on Tab
		if event.key() == Qt.Key.Key_Tab:
			self.reset()

	def processInput(self, text: str) -> None:
		if not text:
			return	
		if text[-1] == ' ':
			if self.current_index == len(self.current_words):
				self.textbox.clear()
			else:
				highlight = Highlight.RIGHT if text[:-1] == self.current_words[self.current_index].text else Highlight.WRONG
				self.label.setText(self.prepareText(self.current_words, self.current_index, highlight))
				self.current_index += 1
				self.textbox.clear()

	def prepareText(self, words: list[Word], index: int, highlight: Highlight) -> str:
		words[index].highlight = highlight
		if highlight != Highlight.UPCOMING and index + 1 < len(words):
			words[index + 1].highlight = Highlight.UPCOMING
		return ' '.join([str(word) for word in words])

	def reset(self) -> None:
		self.current_index = 0
		self.current_words = self.getWords(10)
		self.current_word = self.current_words[0]
		self.label.setText(self.prepareText(self.current_words, 0, Highlight.UPCOMING))
		self.textbox.clear()

	def getWords(self, size: int) -> list[Word]:
		lang = getLayout()
		if lang  == 'en':
			return random.sample(list(map(lambda w: Word(w), english_words)), size)
		return random.sample(list(map(lambda w: Word(w), russian_words)), size)

if __name__ == '__main__':
	app = QApplication([])

	screen = app.primaryScreen()
	rect = screen.availableGeometry()

	window = Window(rect.width(), rect.height())
	app.exec_()

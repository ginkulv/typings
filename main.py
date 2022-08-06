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
	RIGHT = 0
	WRONG = 1
	UPCOMING = 2

def getLayout() -> str:
	layout = ctypes.windll.user32.GetKeyboardLayout(0)
	# 67699721 -> en
	# 68748313 -> ru
	if layout == 67699721:
		return 'en'
	return 'ru'

class Window(QMainWindow):
	current_index = 0
	current_words = []
	sample_size = 10

	def __init__(self, width: int, height: int):
		super().__init__()

		# Set up words
		window_width, window_height = int(width * 0.6), 400
		self.current_words = self.getWords(self.sample_size)

		# Set up window
		self.setWindowOpacity(0.9)
		self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
		self.setGeometry(int(width * 0.2), height // 2, window_width, window_height)
		self.setStyleSheet('background-color: #808080')

		# Set up label for words
		self.label = QLabel(self.prepareText(self.current_words, 0, Highlight.UPCOMING), self)
		# self.label = QLabel('word <b style="color: #0000FF;">word</b>', self)
		self.label.setFont(QFont('Hack NF'))
		self.label.move(150, 200)
		self.label.setGeometry(int(window_width * 0.2), 0, int(window_width * 0.6), self.height())
		self.label.setWordWrap(True)
		self.label.setStyleSheet('color: black; font-size: 28px')

		# Set up textbox
		self.textbox = QLineEdit(self)
		self.textbox.move(int(width * 0.2), window_height - 40)
		self.textbox.installEventFilter(self)
		self.textbox.textChanged.connect(self.processInput)

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
			if self.current_index >= len(self.current_words):
				self.textbox.clear()
			else:
				self.current_index += 1
				highlight = Highlight.RIGHT if text[:-1] == self.current_words[self.current_index] else Highlight.WRONG
				self.label.setText(self.prepareText(self.current_words, self.current_index, highlight))
				self.textbox.clear()

	def prepareText(self, arr: list[str], index: int, highlight: Highlight) -> str:
		colors = {
			Highlight.RIGHT: "#7CFC00",
			Highlight.WRONG: "#FF00FF",
			Highlight.UPCOMING: "#89CFF0"
		}
		arr[index] = f'<b style="color: {colors[highlight]};">{arr[index]}</b>'
		return ' '.join(arr)


	def reset(self) -> None:
		self.current_index = 0
		self.current_words = self.getWords(10)
		self.current_word = self.current_words[0]
		self.label.setText(self.prepareText(self.current_words, 0, Highlight.UPCOMING))
		self.textbox.clear()

	def getWords(self, size: int) -> list[str]:
		lang = getLayout()
		if lang  == 'en':
			return random.sample(english_words, size)
		return random.sample(russian_words, size)

if __name__ == '__main__':
	app = QApplication([])

	screen = app.primaryScreen()
	rect = screen.availableGeometry()

	window = Window(rect.width(), rect.height())
	app.exec_()

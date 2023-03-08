import sys
import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets, QtGui, QtCore


class SentimentAnalyzer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize the UI
        self.setWindowTitle('Sentiment Analyzer')
        self.setGeometry(100, 100, 800, 600)
        self.text_label = QLabel()
        self.text_label.setFont(QFont('Arial', 14))
        self.text_label.setAlignment(QtCore.Qt.AlignTop)
        self.text_font = QtGui.QFont()
        self.text_font.setPointSize(30)
        self.text_font.setBold(True)
        self.text_label.setFont(self.text_font)
        self.text_label1 = QLabel()
        self.text_label1.setFont(QFont('Arial', 12))
        self.text_label1.setAlignment(QtCore.Qt.AlignTop)
        self.text_font1 = QtGui.QFont()
        self.text_font1.setPointSize(20)
        self.text_font1.setBold(True)
        self.text_label1.setFont(self.text_font1)
        self.welcome_label = QLabel()
        self.welcome_label.setFont(QFont('Arial', 14))
        self.welcome_label.setText("Welcome to\n Sentiment Analysis Program")
        self.welcome_label.setGeometry(50, 50, 700, 100)
        self.welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        self.welcome_font = QtGui.QFont()
        self.welcome_font.setPointSize(30)
        self.welcome_font.setBold(True)
        self.welcome_label.setFont(self.welcome_font)
        self.sentiment_button = QPushButton('Analyze Sentiment')
        self.sentiment_button.setFont(QFont('Arial', 14))
        self.sentiment_button.clicked.connect(self.analyze_sentiment)
        self.graph_button = QPushButton('Show Emotion Graph')
        self.graph_button.setFont(QFont('Arial', 14))
        self.graph_button.clicked.connect(self.show_graph)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.text_label1)
        self.layout.addWidget(self.welcome_label)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.sentiment_button)
        self.button_layout.addWidget(self.graph_button)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.text = open('read.txt', encoding='utf-8').read()
        self.lower_case = self.text.lower()
        self.cleaned_text = self.lower_case.translate(str.maketrans('', '', string.punctuation))

        self.emotions = self.load_emotions()

    
    def load_emotions(self):
        emotions = {}
        with open('emotions.txt', 'r') as file:
            for line in file:
                clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')
                emotions[word] = emotion
        return emotions

    def preprocess_text(self, text):
        # Convert to lowercase and remove punctuation
        cleaned_text = text.lower().translate(str.maketrans('', '', string.punctuation))

        # Tokenize words and remove stop words
        tokenized_words = word_tokenize(cleaned_text, "english")
        final_words = [word for word in tokenized_words if word not in stopwords.words('english')]

        # Lemmatize words
        lemma_words = [WordNetLemmatizer().lemmatize(word) for word in final_words]

        return lemma_words
    
    def analyze_sentiment(self):
        lemma_words = self.preprocess_text(self.text)

        # Calculate sentiment score using NLTK's SentimentIntensityAnalyzer
        score = SentimentIntensityAnalyzer().polarity_scores(self.cleaned_text)
        print(self.cleaned_text)
        print(score)
        # Determine the sentiment label based on the score
        if score['neg'] > score['pos'] and score['neu'] < score['neg']:
            sentiment_label = "Negative Sentiment"
            score1 = score['neg']
        elif score['neg'] < score['pos'] and score['neu'] < score['pos']:
            sentiment_label = "Positive Sentiment"
            score1 = score['pos']
        elif score['neu'] > score['pos'] and score['neu'] > score['neg']:
            sentiment_label = "Neutral Sentiment"
            score1 = score['neu']
            
        # Display the sentiment label on the UI
        self.text_label.setText(" The Sentiment of the taken Dataset is:  "+sentiment_label)
        self.text_label1.setText(" The Percentage of "+ sentiment_label + "\n in taken Dataset is: "+str(score1*100))
        
    def show_graph(self):
        lemma_words = self.preprocess_text(self.text)
        print(lemma_words)
        # Count the number of occurrences of each emotion in the text
        emotion_list = []
        with open('emotions.txt', 'r') as file:
            for line in file:
                clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')

                if word in lemma_words:
                    emotion_list.append(emotion)

        # emotion_list = emotion_list.translate(str.maketrans('', '', string.punctuation))
        # print(emotion_list)
        emotion_counts = Counter(emotion_list)
        print(emotion_counts)

        # Plot the emotion count graph
        fig, ax1 = plt.subplots()
        ax1.bar(emotion_counts.keys(), emotion_counts.values())
        fig.autofmt_xdate()
        plt.savefig('graph.png')
        plt.show()


# if __name__ == '__main__':
#     app = QApplication([])
#     window = SentimentAnalyzer()
#     window.show()
#     sys.exit(app.exec_())


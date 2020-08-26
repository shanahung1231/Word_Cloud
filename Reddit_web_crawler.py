import matplotlib.pyplot as plt

import nltk # Natural Language ToolKit
nltk.download('stopwords')
from nltk.corpus import stopwords # to get rid of StopWords 
# Initialize the stopwords
stopwords_l = stopwords.words('english')  #list
print(stopwords_l)
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator # to create a Word Cloud
from PIL import Image # Pillow with WordCloud to image manipulation
from urllib.parse import urlparse, parse_qs, quote, urljoin
from collections import Counter
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


import csv
import datetime as dt
import praw
import pandas as pd


class RedditCrawler():
    def __init__(self):
        pass
    
    def show_img(self, board, limit_num):
        reddit = praw.Reddit(client_id='EwAVjgascYrGIg', client_secret='Z7HahaiGdEKl3e57vml1VkC0pVc', user_agent='hunghunghung1231')

        subreddit = reddit.subreddit(board) #input what subreddit you want to search for
        top_subreddit = subreddit.top()   # grab most up-voted topics all-time
        top_subreddit = subreddit.hot(limit=limit_num)  #使用者輸入要爬幾篇文章
        # for submission in subreddit.top(limit=limit_num):
        #     print(submission.title, submission.id)
        topics_dict = { "title":[], "score":[], "id":[], "url":[],  "comms_num": [], "created": [], "body":[]}
        for submission in top_subreddit:
            topics_dict["title"].append(submission.title)
            topics_dict["score"].append(submission.score)
            topics_dict["id"].append(submission.id)
            topics_dict["url"].append(submission.url)
            topics_dict["comms_num"].append(submission.num_comments)
            topics_dict["created"].append(submission.created)
            topics_dict["body"].append(submission.selftext)
        topics_data = pd.DataFrame(topics_dict)

        def get_date(created):
            return dt.datetime.fromtimestamp(created)

        _timestamp = topics_data["created"].apply(get_date)
        topics_data = topics_data.assign(timestamp = _timestamp)
        comment_string = ''  #set an dict to count words
        word_list = []
        for word in topics_data['title']:
            comment_string += word

        stopwords = set(stopwords_l)
        stopwords.add('https')
        stopwords.add('gif')
        wc = WordCloud(height=500, width=1000, background_color='white', stopwords=stopwords).generate(comment_string)
        img = wc.to_file('img.png')
        plt.imshow(img)
        plt.axis("off")
        plt.show()


#     def generate_cloud(self, count_dict):
#         # font = '/System/Library/Fonts/STHeiti Medium.ttc'
#         font = 'STHeiti Medium.ttc'
#         my_wordcloud = WordCloud(font_path=font)
#         my_wordcloud.generate_from_frequencies(frequencies=count_dict)
#         plt.imshow(my_wordcloud)
#         plt.axis("off")
#         plt.show()


class UserInterface(GridLayout):
    def __init__(self):
        super().__init__()
        self.cols = 2
        self.rows = 3
        self.add_widget(Label(text="Please enter which board to crawl"))
        self.board = TextInput(multiline=False)
        self.add_widget(self.board)
        self.add_widget(Label(text="How many articles to crawl (ex: 100, 200, 300...)"))
        self.amount = TextInput(multiline=False)
        self.add_widget(self.amount)
        self.run = Button(text='Run')
        self.run.bind(on_press=self._run_crawler)
        self.add_widget(Label())
        self.add_widget(self.run)
        self.pop_up = Popup(title='Waring', content=Label(text='Input amount must be integer'), size_hint=(None, None),
                            size=(400, 400))

    def _run_crawler(self, instance):
        # try:
        #     pages = int(self.amount.text) // 10
        # except Exception:

        #     self.pop_up.open()
        #     return
        my_crawler = RedditCrawler()
        my_crawler.show_img(self.board.text, int(self.amount.text))


class TestApp(App):
    def build(self):
        self.title = "Word Cloud Generator"
        return UserInterface()


if __name__ == "__main__":
    TestApp().run()



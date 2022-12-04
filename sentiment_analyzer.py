import praw
from praw.models import MoreComments
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import ssl
import numpy as np

class SentimentAnalyzer:
  def __init__(self):
    # Initialize API for accessing Reddit
    self.reddit = praw.Reddit(client_id='ztDxQYjz7r13ehVGDa4mJw', client_secret='leSNrLkS81iXQq1JHwgWGP4kgFk4FA', user_agent='sentimentAnalysisScraper')

    # Initalize sentiment analyzer
    # Credit to https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed for the below snippet to avoid CERTIFICATE_VERIFY_FAILED error
    try:
      _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
      pass
    else:
      ssl._create_default_https_context = _create_unverified_https_context
      nltk.download('vader_lexicon')

    self.sentiment_analyzer = SentimentIntensityAnalyzer()
  
  def analyze_threads(self, thread_urls, user_flair=None, include_replies=False, include_only_top_comments=True):
    return_obj = {
      "avg_pos": [],
      "avg_neg": [],
      "thread_titles": [],
      "most_pos_comments": [],
      "most_neg_comments": [],
    }

    # Iterate over each provided thread
    for thread_url in thread_urls:
      print("Retrieving comments from " + thread_url)
      thread = self.reddit.submission(url=thread_url)
      if not include_only_top_comments:
        thread.comments.replace_more(limit=None) # Expands comment set to include more than just top upvoted comments. May increase runtime

      # Check if we want to include comments that are replies to other comments
      if include_replies:
        comments = thread.comments.list()
      else:
        comments = thread.comments

      # Check if we only want to keep comments with a specific user flair
      if user_flair:
        comments = [c for c in comments if (not isinstance(c, MoreComments)) and c.author_flair_text and user_flair in c.author_flair_text]

      num_comments = len(comments)
      pos_counter = 0
      neg_counter = 0

      # Analyze sentiment of each comment
      analyzed_comments = []
      pos_scores = []
      neg_scores = []
      for comment in comments:
        if not isinstance(comment, MoreComments):
          sentiment_scores = self.sentiment_analyzer.polarity_scores(comment.body)
          pos_score = sentiment_scores["pos"]
          neg_score = sentiment_scores["neg"]
          pos_counter += pos_score
          neg_counter += neg_score
          analyzed_comments.append(comment.body)
          pos_scores.append(pos_score)
          neg_scores.append(neg_score)

      # Store results
      return_obj["avg_pos"].append(pos_counter / num_comments)
      return_obj["avg_neg"].append(neg_counter / num_comments)
      return_obj["thread_titles"].append(thread.title)
      return_obj["most_pos_comments"].append(analyzed_comments[np.argmax(pos_scores)])
      return_obj["most_neg_comments"].append(analyzed_comments[np.argmax(neg_scores)])

    return return_obj

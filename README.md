# Documentation - Sentiment Analyzer for the College Football Subreddit

## Project Overview
For my course project, I developed an application that performs sentiment analysis on post-game threads from the college football subreddit to assess the progression of fan sentiment over the course of a season.

These post-game threads provide an interesting opporunity for sentiment analysis because they are an open forum for fans to discuss their thoughts about the game and their team. Additionally, by looking at flairs, one can identify which team a user is a fan of, which provides further insight that we can extract when performing sentiment analysis. Thus, when we analyze multiple threads across the season, we will be able to track how fan sentiment changed over the course of a season.

As an example, here (https://www.reddit.com/r/CFB/comments/z5liww/postgame_thread_illinois_defeats_northwestern_413/) is the post-game thread from Illinois's recent 41-3 victory over Northwestern in their regular season finale.

## Code Overview
The code for this project is contained in two main files: `sentiment_analyzer.py` and `app.py`.

`sentiment_analyzer.py` contains all the code for performing sentiment analysis. There, a `SentimentAnalyzer` class is defiend, where the `analyze_threads` method will perform sentiment analysis on the provided post-game thread URLs. There are additional optional configurations to this method in which a user can specify whether to filter comments based on user flair (in order to only include comments from fans of a certain team), whether to include replies to other comments, and whether to only include top / highly upvoted comments on the post. The analyzer pulls comments from reddit using the PRAW API. Once it retrieves and filters the comments from each thread, it analyzers the sentiment of each comment using the `SentimentIntensityAnalyzer` module from the NLTK library. In particular, I use NLTK's pre-trained analyzer called VADER, which is well-suited for langage used in social media. The analyzer provides a positive, negative, and neutral score to each comment, and then my code averages all positive and negative scores for each thread. It also extracts the most positive and most negative comment from each thread. 

`app.py` is the main driver of my application. Here, a Flask app is initalized, which provides the UI. The code first directs the user to a screen where they can select which threads to analyze. Once selected, I call my `SentimentAnalyzer` class and analyze the threads. After it finishes, results of the analysis will be displayed in the UI.

## Outcome / Application Workflow
The user is first brought to a screen where they specify the input settings of which threads will be analyzed, and how those threads should be analyzed. First, in the "Thread Selection" section, a user can either choose one of the pre-selected teams and analyze the post-game threads over the course of the season for that team, or provide their own threads. Only one of these two user paths should be taken. If a user decides to enter their own threads, they can find a directory of all post-game threads to find the appropriate links. Each link should be entered separately on a new line, and the team name that the user enters should match how it is written on the reddit post-game thread directory.

After specifying these links, the user can choose some specific analysis settings. In particular, they can choose whether to only include comments whose flair matches the team they've chosen to analyze, whether to include comments that are replies, and whether to only include highly upvoted comments. Default selections are already specified for these options. 

Lastly, a user can choose 1 of 3 output settings. Specifically, they can choose to view the trend of both positive and negative sentiment, just positive sentiment, or just negative sentiment. 

With all settings specified, a user can hit the "Submit" button to trigger the actual sentiment analysis. Progress of the analysis can be monitored in the terminal / command line window from which the application was launched. Once the analysis is complete, a new page will render displaying the titles of all threads that were analyzed, the most positive and negative comment from each, the overall most positive and negative game, and a line graph of polarity scores to track how sentiment shifted across the season.


## Setup Option 1 - Running the application using Docker
In order to spin up the application with Docker, please follow these steps:
1. Run `docker build --tag cfb-analyzer-project .` in the command line. Please note to include the period (`.`) at the end of the command.
2. Run `docker run -p 5000:5000 -e PYTHONUNBUFFERED=1 cfb-analyzer-project` in the command line.
3. Go to `http://127.0.0.1:5000/` in browser.

## Setup Option 2 - Running the application without Docker
In order to spin up the application without Docker, please follow these steps:
1. Run `pip install -r requirements.txt` or `pip3 install -r requirements.txt` in the command line.
2. Run `python app.py` or `python3 app.py` in the command line.
3. Go to `http://127.0.0.1:5000/` in browser.

## Self-Evaluation
I have indeed completed all aspects of my project that I originally intended to. Overall, I am quite pleased with the outcome of my project, as the resulting application is inuitive to use and clearly displays how fan sentiment shifted across the season. Moreover, the actual sentiment analysis results generally seem to match with what I would expect. For instance, lower scores are usually associated with losses and higher scores typically correspond to wins, thus illustrating the successful performance of the sentiment analyzer.
from urllib import request
from sentiment_analyzer import SentimentAnalyzer
from flask import Flask, request
import numpy as np
from matplotlib.figure import Figure
import base64
from io import BytesIO

# Initalize flask and the sentiment analyzer
app = Flask(__name__)
analyzer = SentimentAnalyzer()

# Store pre-selected post-game threads for 5 different teams
team_dict = {
  "California": [
    "https://www.reddit.com/r/CFB/comments/x57qeo/postgame_thread_california_defeats_uc_davis_3413/",
    "https://www.reddit.com/r/CFB/comments/xb38wq/postgame_thread_california_defeats_unlv_2014/",
    "https://www.reddit.com/r/CFB/comments/xgyymz/postgame_thread_notre_dame_defeats_california_2417/",
    "https://www.reddit.com/r/CFB/comments/xn9flj/postgame_thread_california_defeats_arizona_4931/",
    "https://www.reddit.com/r/CFB/comments/xtb3ji/postgame_thread_washington_state_defeats/",
    "https://www.reddit.com/r/CFB/comments/y4z9if/postgame_thread_colorado_defeats_california_2013/",
    "https://www.reddit.com/r/CFB/comments/yb9lm3/postgame_thread_washington_defeats_california_2821/",
    "https://www.reddit.com/r/CFB/comments/ygxmk8/postgame_thread_oregon_defeats_california_4224/",
    "https://www.reddit.com/r/CFB/comments/ynicb9/postgame_thread_usc_defeats_california_4135/",
    "https://www.reddit.com/r/CFB/comments/ytsjmu",
    "https://www.reddit.com/r/CFB/comments/yzssp4",
    "https://www.reddit.com/r/CFB/comments/z4tuya"
  ],
  "Illinois": [
    "https://www.reddit.com/r/CFB/comments/wzghmy/postgame_thread_illinois_defeats_wyoming_386/",
    "https://www.reddit.com/r/CFB/comments/x4l2av/postgame_thread_indiana_defeats_illinois_2320/",
    "https://www.reddit.com/r/CFB/comments/xb3mjc/postgame_thread_illinois_defeats_virginia_243/",
    "https://www.reddit.com/r/CFB/comments/xlm914/postgame_thread_illinois_defeats_chattanooga_310/",
    "https://www.reddit.com/r/CFB/comments/xt40nn/postgame_thread_illinois_defeats_wisconsin_3410/",
    "https://www.reddit.com/r/CFB/comments/xzaw7z/postgame_thread_illinois_defeats_iowa_96/",
    "https://www.reddit.com/r/CFB/comments/y4w0ah/postgame_thread_illinois_defeats_minnesota_2614/",
    "https://www.reddit.com/r/CFB/comments/ygxd7l/postgame_thread_illinois_defeats_nebraska_269/",
    "https://www.reddit.com/r/CFB/comments/yn9bjm/postgame_thread_michigan_state_defeats_illinois/",
    "https://www.reddit.com/r/CFB/comments/ytictw",
    "https://www.reddit.com/r/CFB/comments/yzlicn",
    "https://www.reddit.com/r/CFB/comments/z5liww"
  ],
  "Kansas": [
    "https://www.reddit.com/r/CFB/comments/x4k4cl",
    "https://www.reddit.com/r/CFB/comments/xb690b",
    "https://www.reddit.com/r/CFB/comments/xh2ba0",
    "https://www.reddit.com/r/CFB/comments/xn1it1",
    "https://www.reddit.com/r/CFB/comments/xt8s61",
    "https://www.reddit.com/r/CFB/comments/xz1co7",
    "https://www.reddit.com/r/CFB/comments/y4wt0h",
    "https://www.reddit.com/r/CFB/comments/yavzsa",
    "https://www.reddit.com/r/CFB/comments/yn95au",
    "https://www.reddit.com/r/CFB/comments/ytqxgl",
    "https://www.reddit.com/r/CFB/comments/yzpr7h",
    "https://www.reddit.com/r/CFB/comments/z5rgi6"
  ],
  "South Carolina": [
    "https://www.reddit.com/r/CFB/comments/x5cei7",
    "https://www.reddit.com/r/CFB/comments/xaye6x",
    "https://www.reddit.com/r/CFB/comments/xgv9xy",
    "https://www.reddit.com/r/CFB/comments/xnbxe8",
    "https://www.reddit.com/r/CFB/comments/xrprnv",
    "https://www.reddit.com/r/CFB/comments/xzam5w",
    "https://www.reddit.com/r/CFB/comments/yb6imj",
    "https://www.reddit.com/r/CFB/comments/ygxsry",
    "https://www.reddit.com/r/CFB/comments/ynf99e",
    "https://www.reddit.com/r/CFB/comments/ytn0zb",
    "https://www.reddit.com/r/CFB/comments/yzuk2d",
    "https://www.reddit.com/r/CFB/comments/z5hddq"
  ],
  "Wake Forest": [
    "https://www.reddit.com/r/CFB/comments/x3q8lg",
    "https://www.reddit.com/r/CFB/comments/xaxjj5",
    "https://www.reddit.com/r/CFB/comments/xh2927",
    "https://www.reddit.com/r/CFB/comments/xn2cru",
    "https://www.reddit.com/r/CFB/comments/xt8xyn",
    "https://www.reddit.com/r/CFB/comments/xzafkb",
    "https://www.reddit.com/r/CFB/comments/yb1382",
    "https://www.reddit.com/r/CFB/comments/ygxo3s",
    "https://www.reddit.com/r/CFB/comments/ynfew8",
    "https://www.reddit.com/r/CFB/comments/ytrf5z",
    "https://www.reddit.com/r/CFB/comments/yzv4ol",
    "https://www.reddit.com/r/CFB/comments/z5lof7"
  ]
}

# Helper function to plot trend of positive and negative sentiment scores
def plot(pos_scores, neg_scores):
  games = np.arange(1, len(pos_scores) + 1)

  fig = Figure()
  ax = fig.subplots()
  if pos_scores:
    ax.plot(games, pos_scores, "g")
  if neg_scores:
    ax.plot(games, neg_scores, "r")
  ax.legend(["Positive", "Negative"])
  ax.set_xlabel("Game Number")
  ax.set_ylabel("Polarity Score")
  ax.set_xticks(games)
  ax.set_title("Polarity Trend Across Games")
  buf = BytesIO() # Method found from https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
  fig.savefig(buf, format="png")
  data = base64.b64encode(buf.getbuffer()).decode("ascii")
  # fig.savefig('plot.png')
  return data

# Helper page to provide links to all post-game threads from the season
@app.route('/thread_directory')
def thread_directory():
  return """
    <html>
      <body>
        <h2>Sentiment Analysis For Post-Game Threads on the College Football Subreddit (reddit.com/r/cfb)</h2>
        <h3>Index of all Post-Game Threads</h2>
        <p>Week 0: <a href="https://www.reddit.com/r/CFB/comments/wz9qmg/week_0_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/wz9qmg/week_0_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 1: <a href="https://www.reddit.com/r/CFB/comments/x4wg2q/week_1_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/x4wg2q/week_1_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 2: <a href="https://www.reddit.com/r/CFB/comments/xargqx/week_2_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/xargqx/week_2_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 3: <a href="https://www.reddit.com/r/CFB/comments/xgoqrc/week_3_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/xgoqrc/week_3_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 4: <a href="https://www.reddit.com/r/CFB/comments/xmv2bh/week_4_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/xmv2bh/week_4_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 5: <a href="https://www.reddit.com/r/CFB/comments/xsxg1i/week_5_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/xsxg1i/week_5_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 6: <a href="https://www.reddit.com/r/CFB/comments/xyuvpi/week_6_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/xyuvpi/week_6_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 7: <a href="https://www.reddit.com/r/CFB/comments/y4q4af/week_7_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/y4q4af/week_7_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 8: <a href="https://www.reddit.com/r/CFB/comments/yapz16/week_8_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/yapz16/week_8_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 9: <a href="https://www.reddit.com/r/CFB/comments/yglu8k/week_9_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/yglu8k/week_9_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 10: <a href="https://www.reddit.com/r/CFB/comments/ymwec2/week_10_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/ymwec2/week_10_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 11: <a href="https://www.reddit.com/r/CFB/comments/ytawna/week_11_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/ytawna/week_11_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 12: <a href="https://www.reddit.com/r/CFB/comments/yzf4pz/week_12_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/yzf4pz/week_12_game_thread_and_postgame_thread_index/</a></p>
        <p>Week 13: <a href="https://www.reddit.com/r/CFB/comments/z5au12/week_13_game_thread_and_postgame_thread_index/" target="_blank">https://www.reddit.com/r/CFB/comments/z5au12/week_13_game_thread_and_postgame_thread_index/</a></p>
      </body>
    </html>
    """

@app.route('/', methods=["GET", "POST"])
def index():
  # If a POST request, display sentiment analysis results
  if request.method == "POST":
    if "team" in request.form:
      team = request.form["team"]
      threads_to_analyze = team_dict[team]
    else:
      team = request.form["team_name"]
      requested_threads = request.form["team_threads"].split("\n")
      threads_to_analyze = []
      for t in requested_threads:
        if t and t[-1] == "\r":
          threads_to_analyze.append(t[:-1].strip())
        elif t and t.strip() != "":
          threads_to_analyze.append(t.strip())

    # Call sentiment analyzer, retrieve results
    result = analyzer.analyze_threads(threads_to_analyze, team if "user_flair" in request.form else None, "include_replies" in request.form, "include_only_top_comments" in request.form)
    pos_trend = result["avg_pos"]
    neg_trend = result["avg_neg"]
    titles = result["thread_titles"]
    pos_comments = result["most_pos_comments"]
    neg_comments = result["most_neg_comments"]
    titles = [s[18:] if "[Postgame Thread]" in s else s for s in titles]
    
    plot_settings = request.form["plot_settings"]
    if plot_settings == "pos_and_neg":
      plot_data = plot(pos_trend, neg_trend)
    elif plot_settings == "pos_only":
      plot_data = plot(pos_trend, None)
    else:
      plot_data = plot(None, neg_trend)

    # Show list of games that was analyzed, as well as the most positive and negative comment from each post-game thread
    list_of_games = "<ol>"
    for i, title in enumerate(titles):
      list_of_games += f"<li>{title}"
      list_of_games += "<ul>"
      list_of_games += f"<li>Most positive comment: {pos_comments[i]}</li>"
      list_of_games += f"<li>Most negative comment: {neg_comments[i]}</li>"
      list_of_games += "</ul>"
      list_of_games += "</li>"
    list_of_games += "</ol>" 

    most_positive_game = "<p>" + titles[np.argmax(pos_trend)] + "</p>" 
    most_negative_game = "<p>" + titles[np.argmax(neg_trend)] + "</p>" 

    return f"""
    <html>
      <body>
        <h2>Sentiment Analysis For Post-Game Threads on the College Football Subreddit (reddit.com/r/cfb)</h2>
        <h3>Games Analyzed</h3>
        {list_of_games}
        <h3>Most Positive Game</h3>
        {most_positive_game}
        <h3>Most Negative Game</h3>
        {most_negative_game}
        <h3>Season-Long Trend of Sentiment</h3>
        <img src='data:image/png;base64,{plot_data}'/>
      </body>
    </html>
    """

  return """
  <html>
    <body>
      <h2>Sentiment Analysis For Post-Game Threads on the College Football Subreddit (reddit.com/r/cfb)</h2>
      <form method="post" id="settings">

        <p><b>Input Settings</b></p>

        <p><i>Thread Selection</i></p>
        <label for="team">Choose a team with pre-selecred threads:</label>
        <select name="team" id="team">
          <option disabled selected value >*Team*</option>
          <option value="California">California</option>
          <option value="Illinois">Illinois</option>
          <option value="Kansas">Kansas</option>
          <option value="South Carolina">South Carolina</option>
          <option value="Wake Forest">Wake Forest</option>
        </select><br>
        <p>Or enter your own threads here:</p>
        <label for="team_name">Team Name:</label><br>
        <input type="text" id="team_name" name="team_name"><br>
        <label for="team_threads">Threads (please enter each URL on a new line, directory of threads can be found <a href="/thread_directory" target="_blank">here</a>):</label><br>
        <textarea name="team_threads" form="settings" style="width:800px; height:100px;"></textarea><br>

        <p><i>Analysis Settings</i></p>
        <input type="checkbox" id="user_flair" name="user_flair" value="user_flair" checked>
        <label for="user_flair">Filter comments based on flair of selected team</label><br>

        <input type="checkbox" id="include_replies" name="include_replies" value="include_replies">
        <label for="include_replies">Include comments that are replies to other comments</label><br>

        <input type="checkbox" id="include_only_top_comments" name="include_only_top_comments" value="include_only_top_comments" checked>
        <label for="include_only_top_comments">Include only top (highly upvoted) comments. Warning: de-selecting this option will increase runtime.</label><br>


        <p><b>Output Settings</b></p>
        
        <input type="radio" id="pos_and_neg" name="plot_settings" value="pos_and_neg" style="margin-left:13px;" checked>
        <label for="pos_and_neg">Display both positive and negative sentiment trends</label><br>
        <input type="radio" id="pos_only" name="plot_settings" value="pos_only">
        <label for="pos_only">Display only positive sentiment trend</label><br>
        <input type="radio" id="neg_only" name="plot_settings" value="neg_only">
        <label for="neg_only">Display only negative sentiment trend</label><br>

        <br>
        <input type="submit" value="Submit">
      </form>
    </body>
  </html>
  """
if __name__ == "__main__":
  app.run(host='0.0.0.0')
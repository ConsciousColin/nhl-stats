import os

from flask import Flask, request
from nhl_stats.write_stats import teams
from nhl_stats.write_stats import players
from nhl_stats.write_stats import games

app = Flask(__name__)


@app.route("/teams/write")
def write_teams_data():
    teams.write_team_data(season=request.args.get('season'))
    return "Success!"


@app.route("/players/write")
def write_players_data():
    players.write_players_data(season=request.args.get('season'))
    return "Success!"


@app.route("/games/write")
def write_games_data():
    games.write_games_data(season=request.args.get('season'))
    return "Success!"

if __name__ == "__main__":
    app.run(debug=False, 
            host="0.0.0.0", 
            port=int(os.environ.get("PORT", 8080)))
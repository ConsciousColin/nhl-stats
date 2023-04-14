import os

from flask import Flask, request
from nhl_stats.write_stats import teams

app = Flask(__name__)


@app.route("/teams/write")
def write_teams_data():
    teams.write_team_data(season=request.args.get('season'))
    return "Success!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
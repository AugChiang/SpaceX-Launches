from flask import Flask, render_template
from datetime import datetime
import requests

# init a flask obj
app = Flask(__name__)

# run this py file directly,
# rather than import into another file
# not utilized by other python file.

@app.route("/")
def index():
    # make data available via 'launches' var
    return render_template("index.html", launches=launches)


@app.template_filter("date_only")
def date_only_filters(s):
    dateobj = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dateobj.date()


# using api to retrieve SpaceX launch data
# https://github.com/r-spacex/SpaceX-API

def get_spacex_launches():
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url=url)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def categorize_launches(launches):
    success = list(filter(lambda x: x['success'] and not x['upcoming'], launches))
    fail = list(filter(lambda x: not x['success'] and not x['upcoming'], launches))
    upcoming = list(filter(lambda x: x['upcoming'], launches))
    return {
        "successful":success,
        "failed": fail,
        "upcoming": upcoming
    }

launches = categorize_launches(get_spacex_launches())


if __name__ == "__main__":
    app.run(debug=True)
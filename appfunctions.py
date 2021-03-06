import datetime as dt
import imdb
import json

imdb_access = imdb.IMDb()

class Movie:
    """
    basic unit for storing movies as poll results
    """
    def __init__(self, title):
        self.title = title
        self.imdbURL = imdb_access.get_imdbURL(
            imdb_access.search_movie(title)[0]
        )
        self.watchURL = None
        self.votes = set()

    def updateURL(self, imdbURL=None, watchURL=None):
        """
        this is used to update watch or imd urls when they are not pointing to the right place.
        :param imdbUrl: this can be populated with a string that will replace the current imdburl as long as the string
        is not empty
        :param watchUrl: this can be populated with a string that will replace the current watchurl as long as the string
        is not empty
        :return: this is not a functional method
        """
        if imdbUrl:
            if isinstance(imdbUrl, str):
                self.imdbURl = imdbUrl
        if watchUrl:
            if isinstance(watchUrl, str):
                self.imdbURl = watchUrl

    def vote(self, name):
        """
        this will toggle votes from a name
        :return: not functional
        """
        if name in self.votes:
            self.votes.remove(name)
            return
        self.votes.add(name)

    def clearVotes(self):
        """
        this will clear all votes from a movie
        :return: not functional
        """
        self.votes = []


def next_time(target):
    date = dt.datetime.now()
    next_min = date + dt.timedelta(minutes=(target["minutes"] - date.minute + 60) % 60)
    next_hr = next_min + dt.timedelta(hours=(target["hours"] - next_min.hour + 24) % 24)
    return next_hr + dt.timedelta(days=(target["days"] - next_hr.weekday() + 7) % 7)


def make_poll_view(movies):
    watchornot = lambda wurl: "NOT AVAILABLE" * bool(not wurl) + "*<Watch @|{}>*".format(wurl) * bool(wurl)
    view = {}
    view["type"] = "home"
    view["callback_id"] = "home_view"
    view["blocks"] = []
    view["blocks"].append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Movie for next Sunday:*"
            }
        }
    )
    view["blocks"].append({
        "type": "divider"
    })
    for movie in movies:
        view["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "{}".format(movie.title)
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Sounds Good!"
                    },
                    "value": "{} vote".format(movie.title)
                }
            }
        )
        view["blocks"].append(
            {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*<{}|imdb>*".format(movie.imdbURL)
                },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "I am so smart and this is wrong"
                },
                "value": "imdb change button {}".format(movie.title)
                }
            }
        )
        view["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "{}".format(watchornot(movie.watchURL))
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "I am so smart and this is wrong"
                    },
                    "value": "watch change button {}"
                }
            }
        )
        context = {
            "type": "context",
            "elements":[]
        }
        #view["blocks"].append(context)
        view["blocks"].append({
            "type": "divider"
        })
    view["blocks"].append(
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Add a suggestion"
                    },
                    "value": "click_me_123"
                }
            ]
        }
    )
    return view


if __name__ == "__main__":
    movies = []
    movies.append(Movie("Bill and Teds Excellent Adventure"))
    movies.append(Movie("Mars Attacks"))
    movies.append(Movie("raising arizona"))
    parsed = json.dumps(make_poll_view(movies), indent=2, sort_keys=True)
    print(parsed)



"""
{
			"type": "input",
			"block_id": "input123",
			"label": {
				"type": "plain_text",
				"text": "Label of input"
			},
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_input",
				"placeholder": {
					"type": "plain_text",
					"text": "Enter some plain text"
				}
			}
		}
"""
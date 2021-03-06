import os
from slack_bolt import App
import config
import appfunctions as f

movies = []
movies.append(f.Movie("Bill and Teds Excellent Adventure"))
movies.append(f.Movie("Mars Attacks"))
movies.append(f.Movie("raising arizona"))

app = App(
    token=config.tester["auth"],
    signing_secret=config.tester["signing"]
)



f.next_time({"days":7, "hours":14, "minutes": 30})

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view=f.make_poll_view(movies)
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

@app.event("reaction_added")
def event_test(body, say, logger):
    url_reply = "hey there"
    logger.info(body)
    say(url_reply)

def main():
    app.start(port=int(os.environ.get("PORT", 3000)))


if __name__ == "__main__":
    main()
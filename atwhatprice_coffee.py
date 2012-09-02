#!/usr/bin/env python
# Copyleft 2012 Western Cape Labs
# http://www.westerncapelabs.com
# App URL: http://atwhatprice.org

"""
A little test app to capture aveage coffee prices from around the world using humanio
Results will be shown at atwhatprice.org
"""

import humanio
import riak
import uuid, calendar, datetime

# You need a my_humanio_auth.py containing two variables, developer_id and secret_key, 
# which you received when creating your developer account (http://human.io/developer).
import my_humanio_auth

# Define your data storage
RIAK_HOST = '127.0.0.1'
#RIAK_PORT = 8098
RIAK_PORT = 8087
RIAK_PREFIX ='riak'
RIAK_TRANSPORT_CLASS=riak.RiakPbcTransport
RIAK_ANSWER_BUCKET = 'atwhatprice_coffee'
grc = riak.RiakClient(host=RIAK_HOST, port=RIAK_PORT, prefix=RIAK_PREFIX, transport_class=RIAK_TRANSPORT_CLASS)


def main():
	"""Connect to the human.io server, and create an application."""
	# echo into the console
	print "Getting API..."
	app = humanio.App(my_humanio_auth.developer_id,
					my_humanio_auth.secret_key,
					public=True)

	# echo into the console
	print "\nFinding human..."
	app.create_task(description="At What Price: Coffee",
    				humans_per_item=-1, human_can_do_multiple=True,
					on_connect_fn=on_connect, on_finished_fn=on_finished,
					on_submit_fns={"submit": on_submit, "confirm": on_confirm})

	app.start_loop()


def on_connect(session, task, item):
	"""This is called when the human clicks on our task in his client app."""
	session.set_form_name("submit")

	session.add_title("At What Price: Coffee")
	session.add_text("Just a little tool to collect prices of everyday things from around the world")
	session.add_text("We'll map, graph and release the data we collect!")
	session.add_text("")
	session.add_text("This survey is about the worlds drug of choice: coffee!")
	session.add_text("")

	session.add_text("What type of coffee is it?")
	session.add_radio_button("coffee_type", "latte", "Latte")
	session.add_radio_button("coffee_type", "cappo", "Cappuccino")
	session.add_radio_button("coffee_type", "ameri", "Americano")
	session.add_radio_button("coffee_type", "espre", "Espresso")
	session.add_radio_button("coffee_type", "flatw", "Flat White")
	session.add_radio_button("coffee_type", "other", "Other")
	session.add_text("")

	session.add_text("What size is it?")
	session.add_radio_button("coffee_size", "s", "Small")
	session.add_radio_button("coffee_size", "m", "Medium")
	session.add_radio_button("coffee_size", "l", "Large")
	session.add_text("")

	# How much?
	session.add_text("What was the price? (include currency)")
	session.add_text_field("what_price")

	session.add_text("How would you rate the coffee?")
	session.add_rating_selector("coffee_rating", number_of_stars=2)


	# if session.latitude and session.longitude:
	# 	session.add_map(session.latitude, session.longitude, zoom=14, show_marker=True)
	# else:
	# 	session.add_text("No geolocation - not showing map")
	# session.add_text("")

	session.add_submit_button()
	session.add_text("")


def on_submit(session, task, form_data):
	"""This will be called when someone hits the "Submit" button
	created above.  We're going to display their submitted data so
	they can confirm.  This shows that you can build multi-step
	interactions."""
	# echo into the console
	print "Results:"
	print repr(form_data)

	session.clear_screen()

	answer = {
		"added": calendar.timegm(datetime.datetime.utcnow().timetuple()),
		"coffee_type": form_data.get("coffee_type", "(none)"),
		"coffee_size": form_data.get("coffee_size", "(none)"),
		"what_price": form_data["what_price"],
		"coffee_rating": form_data.get("coffee_rating", 0),
		"latitude": session.latitude,
		"longitude": session.longitude
	}
	# Choose a bucket to store our data in 
	answers = grc.bucket(RIAK_ANSWER_BUCKET)
	# Supply a key to store our data under
	key = uuid.uuid1().hex
	newanswer = answers.new(key, data=answer)
	newanswer.store()

	session.add_text("Thanks!")
	session.add_text("")
	session.add_text("We'll show the data we collect at:")
	session.add_link("http://atwhatprice.org")

	session.set_form_name("confirm")

	# Bye.
	session.add_text("")
	session.add_text("Click OK to leave this task")
	session.add_submit_button("OK", "ok")

def on_confirm(session, task, form_data):
	"""Handle the confirmation step from above."""
	# if form_data["submit_button"] == "ok":
	# 	# echo into the console
	# 	print "Thanks... bye!"
	# else:
	# 	print "Never mind... bye!"

	# And now we're done.
	session.dismiss(approve=True)


def on_finished(task):
    print "All done."
    task.app.stop_loop()


if __name__ == "__main__":
    main()
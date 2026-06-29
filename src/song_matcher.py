def match_songs(
    song1_events,
    song2_events
):

    matches = []

    for event1 in song1_events:

        for event2 in song2_events:

            if (
                event1["type"]
                ==
                event2["type"]
            ):

                matches.append({

                    "song1_time":
                    event1["time"],

                    "song2_time":
                    event2["time"],

                    "event_type":
                    event1["type"]

                })

    return matches
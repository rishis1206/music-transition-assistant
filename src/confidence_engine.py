def calculate_confidence(events):
    """
    Uses confidence already calculated inside
    event_classifier instead of fake values.
    """

    scored_events = []

    for event in events:

        scored_events.append({

            "time": event["time"],

            "type": event["type"],

            "confidence": round(
                event.get("confidence", 0) * 100,
                1
            )

        })

    return scored_events
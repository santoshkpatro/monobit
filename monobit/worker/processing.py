def process_payload(payload):
    """
    Error ingestion pipeline.

    Steps:
    1. Normalize payload
    2. Fingerprint / group event
    3. Persist to database
    """

    event = normalize(payload)
    grouped_event = group_event(event)
    store_event(grouped_event)


def normalize(payload):
    """
    Validate and normalize incoming error event.
    """
    return payload


def group_event(event):
    """
    Deduplicate or fingerprint logic.
    """
    return event


def store_event(event):
    """
    Persist event into your Error / Issue models.
    """
    pass

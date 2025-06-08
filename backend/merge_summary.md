# Merge Summary

## metrics.py

- The file defines a FastAPI router using `APIRouter`.
- A single endpoint `/metrics` is implemented.
- The `/metrics` endpoint returns Prometheus metrics.
- The response from the `/metrics` endpoint is formatted with the appropriate Prometheus content type using `CONTENT_TYPE_LATEST`.
- The Prometheus metrics are generated using the `generate_latest` function from the `prometheus_client` library.

---

## models.py

- The file defines a SQLAlchemy model named `Reminder`.
- The `Reminder` class inherits from `Base`, which is a declarative base for SQLAlchemy models.
- The `Reminder` model corresponds to a database table named 'reminders'.
- The model includes the following columns:
  - `id`: An integer serving as the primary key.
  - `user_id`: An integer that cannot be null, representing the user associated with the reminder.
  - `action`: A non-nullable string describing the action to be reminded of.
  - `fire_at`: A non-nullable DateTime indicating when the reminder should trigger.
  - `raw_text`: A non-nullable text field containing the original reminder text.
  - `is_active`: A boolean indicating if the reminder is active, defaulting to `True`.
  - `status`: A string representing the reminder's status, with a default value of "scheduled". Possible values include "scheduled", "fired", and "failed".
  - `created_at`: A DateTime field that defaults to the current UTC time, indicating when the reminder was created.

---

## reminder_parser.py

- Imports the `re`, `datetime`, and `dateparser` modules for regular expressions, date handling, and natural language date parsing, respectively.
- Defines a function `parse_reminder_intent` that takes a string `text` as input.
- Uses a regular expression to naively extract the action verb following "remind me to" in the input text.
- Attempts to parse a datetime from the input text using the `dateparser` library.
- Raises a `ValueError` if the datetime cannot be parsed.
- Returns a dictionary containing:
  - The extracted action (or "unknown" if not found).
  - The parsed datetime.
  - A `repeat` key initialized to `None`.
  - The original input text under the `raw_text` key.

---

## sheduler.py

- Imports the `Reminder` model, `Counter` from `prometheus_client`, and `Session` from `sqlalchemy.orm`.
- Defines two Prometheus counters: `reminders_fired` and `reminders_failed` to track the total number of reminders triggered and failed, respectively.
- Implements a function `schedule_reminder` that takes `reminder_data`, a database session `db`, and a `user_id` as parameters.
- Within `schedule_reminder`, creates a new `Reminder` object using the provided data.
- Adds the new `Reminder` object to the database session and commits the transaction.

---

## tasks.py

- A Celery application named "reminders" is initialized.
- A Celery beat schedule is configured to run the task `check_due_reminders` every 60 seconds.
- The `check_due_reminders` task is defined to:
  - Open a database session.
  - Query the `Reminder` model for reminders that are due to be fired, are active, and have a status of "scheduled".
  - Iterate over the due reminders and attempt to execute a placeholder notification logic.
  - Update the reminder's status to "fired" if successful, or "failed" if an exception occurs.
  - Increment corresponding metrics (`reminders_fired` or `reminders_failed`) based on the outcome.
  - Commit the changes to the database.

---


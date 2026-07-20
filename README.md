
# Random Christmas Bot

This Python project automates the process of organizing a Secret Santa event. It randomly assigns each participant one or two recipients and ensures participants do not receive the same recipients from the previous years. The results are sent via email using an SMTP relay, and participant data (names, emails, and previous draw results) are managed in a CSV file.

## Features

- Randomly assign one or two recipients for each participant.
- Ensure participants do not receive the same recipients as the last `n` years.
- Optional giver/receiver exclusion pairs (e.g. couples who shouldn't draw each other).
- Sends personalized emails with draw results to participants.
- Stores participant data (names, emails, and draw results) in a CSV file.
- Modular structure for better code maintenance.
- All key parameters are configurable via environment variables (`.env`).
- Optional web GUI (FastAPI) to manage participants/exclusions and trigger the draw from a browser.
- Dockerfile + docker-compose for running the web GUI as a container.

## Project Structure

```bash
Random-Christmas-Bot/
│
├── src/
│   ├── draw.py        # Logic for drawing names
│   ├── emailer.py     # Email sending functionality
│   ├── file_io.py     # File handling (CSV reading/writing)
│   ├── main.py        # CLI entry point, exposes run_draw()
│   ├── utils.py       # Utility functions (date, time handling)
│   └── env.py         # Loads configuration from environment variables / .env
│
├── webapp/
│   ├── app.py          # FastAPI app (dashboard, history, draw trigger)
│   ├── templates/      # Jinja2 templates
│   └── static/         # CSS
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example        # Template — copy to .env and fill in real values
└── README.md
```

### Configuration (`.env`)

All configuration is read from environment variables, loaded automatically from a
`.env` file at the repo root if present (via `python-dotenv`) — no secrets live in
tracked source files. Copy `.env.example` to `.env` and fill in your real values:

```bash
# Configuration with SMTP settings and CSV path settings
SMTP_SERVER=smtp.example.com
SMTP_PORT=25
SENDER_EMAIL=santa@example.com
CSV_PATH=path/to/your/csv/files      # Path to the CSV files
CSV_PREFIX=secret_santa_DB            # Prefix for CSV files
HISTORY_YEARS=2                       # Number of past years to consider in the draw
DRAW_PER_PERSON=2                     # Number of recipients per person

# Optional — override the default English email subject/body
# EMAIL_SUBJECT=Secret Santa {year} Draw
# EMAIL_BODY=...

# Optional — protect the web GUI with HTTP basic auth (recommended if exposed beyond localhost)
WEBAPP_USERNAME=admin
WEBAPP_PASSWORD=change-me
```

## Requirements

- Python 3.x
- SMTP server (relay, no authentication required)
- CSV file to store participant data
- Dependencies in `requirements.txt` (`python-dotenv`; `fastapi`/`uvicorn`/`jinja2`/`python-multipart` only needed for the web GUI)

## Installation

1. Clone the repository.
2. Ensure you have Python installed on your system. If not, download and install Python from [here](https://www.python.org/downloads/).
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in the SMTP settings, CSV file path, and draw parameters as needed.

Example structure of the CSV file with the following columns:
```csv
Name,Email,Last_Year_Recipient_1,Last_Year_Recipient_2
```

```csv
Alice,alice@example.com,Bob,Charlie
Bob,bob@example.com,Alice,David
Charlie,charlie@example.com,David,Alice
```

4. Name your CSVs using a consistent naming convention `[prefix]_20xx.csv` as the program will retrieve those using the prefix set in `env.py`.

5. Ensure the CSV file is in the correct location as specified by `CSV_PATH`.

6. (Optional) Add a `[prefix]_exclusions.csv` file with `giver,receiver` rows to prevent
   specific people from being drawn for each other:
   ```csv
   Alice,Bob
   ```

## Usage

1. Create a CSV file for the current year draw with the participants' information (Name and email).
   Like this:
   ```csv
   Alice,alice@example.com
   Bob,bob@example.com
   Charlie,charlie@example.com
   ```

2. Run the main script by executing:

   ```bash
   python src/main.py
   ```

3. The script will:
   - Load participant data from the CSV file.
   - Perform the Secret Santa draw based on the configuration (1 or 2 recipients).
   - Send an email to each participant with the names of their gift recipients.
   - Save the updated draw results back to the CSV file.

4. If any errors occur, they will be displayed in the console, and you can retry or debug as needed.

## Web GUI

Instead of editing CSVs by hand, you can run a small web dashboard to manage
participants and exclusions, view draw history, and trigger the draw from a browser:

```bash
python -m uvicorn webapp.app:app --reload
```

Then open `http://127.0.0.1:8000`. If `WEBAPP_USERNAME`/`WEBAPP_PASSWORD` are set in
`.env`, the whole app is protected with HTTP basic auth; otherwise it's open to
anyone who can reach it — only run it unauthenticated on localhost or a trusted
network. Triggering the draw from the GUI sends real emails and overwrites the
current year's CSV, exactly like running `main.py`.

## Docker

The web GUI can also run as a container:

```bash
cp .env.example .env   # fill in your real values
docker compose up --build -d
```

This builds the image from the `Dockerfile`, starts it on port `8000`, and bind-mounts
`./data` (or `HOST_CSV_PATH` from `.env`) into the container as `/data` — the compose
file forces `CSV_PATH=/data` inside the container regardless of what's in `.env`, so
your CSVs live in that host folder. Stop it with `docker compose down`.

## Customization

- **Number of recipients**: Modify `DRAW_PER_PERSON` in `.env` to choose whether participants receive one or two recipients.
- **Email content**: Customize `EMAIL_SUBJECT`/`EMAIL_BODY` in `.env` using placeholders like `{name}` for the participant's name and `{draws}` for their recipients.
- **CSV file location**: Adjust `CSV_PATH` in `.env` if you prefer a different directory for the participant data.
- **Number of historical years**: Change `HISTORY_YEARS` in `.env` to set how many previous years of draws should be considered.

## File Descriptions

- **`draw.py`**: Contains the logic for performing the Secret Santa draw, ensuring no repeat recipients from the last years and honoring exclusions.
- **`emailer.py`**: Handles email sending via the SMTP server.
- **`file_io.py`**: Responsible for reading and writing participant/exclusion/history data from/to CSV files.
- **`main.py`**: CLI entry point; `run_draw()` loads data, performs the draw, sends emails, and saves results — reused by the web GUI.
- **`utils.py`**: Utility functions, such as fetching the current date and time.
- **`webapp/app.py`**: FastAPI app exposing the dashboard, history view, and draw trigger.

## Notes

- The project assumes an SMTP server that does not require authentication. If authentication is needed, the script can be extended to support login.
- The project should be run once per year before the holiday season.
- Manually update the CSV file each year with any new participants.

## License

This project is licensed under the MIT License. You are free to modify and distribute the script as needed.

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests to improve this project.

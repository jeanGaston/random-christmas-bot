# Random Christmas Bot


This Python project automates the process of organizing a Secret Santa event. It randomly assigns each participant one or two recipients and ensures participants do not receive the same recipients from the previous year. The results are sent via email using an SMTP relay, and participant data (names, emails, and previous draw results) are managed in a CSV file.

## Features

- Randomly assign one or two recipients for each participant.
- Ensure participants do not receive the same recipients as last year.
- Sends personalized emails with draw results to participants.
- Stores participant data (names, emails, and draw results) in a CSV file.
- Modular structure for better code maintenance.
- All key parameters are configurable in a separate configuration file (`env.py`).

## Project Structure

```bash
secret-santa/
│
├── src/
│   ├── draw.py        # Logic for drawing names
│   ├── emailer.py     # Email sending functionality
│   ├── file_io.py     # File handling (CSV reading/writing)
│   ├── main.py        # Main program logic
│   ├── utils.py       # Utility functions (date, time handling)
│   └── env.py         # Configuration settings (SMTP, file paths, etc.)
│
└── README.md          # Project readme
```

### `src/env.py`

The configuration file contains SMTP settings, file paths, and customizable parameters for the draw.

Example `env.py`:

```python
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 25
SENDER_EMAIL = "santa@example.com"
CSV_FILE_PATH = r"secret_santa_DB.csv"
DRAW_PER_PERSON = 2  # Choose 1 or 2 recipients per person

# Email content
EMAIL_SUBJECT = "Secret Santa {year} Draw"
EMAIL_BODY = """
Hello {name},

You have been chosen to give gifts to: {draws}.
Feel free to use your imagination and make their Christmas magical!

Merry Christmas!

This email was sent automatically, please do not reply.
"""
```

## Requirements

- Python 3.x
- SMTP server (relay, no authentication required)
- `smtplib` for sending emails (Python's built-in library)
- CSV file to store participant data

## Installation

1. Clone the repository or download the script files.
2. Ensure you have Python installed on your system. If not, download and install Python from [here](https://www.python.org/downloads/).
3. Set up the `env.py` file in the `src/` directory, adjusting the SMTP settings, CSV file path, and draw parameters as needed.

Example structure of the CSV file
with the following colunms
```csv
Name,Email,Last_Year_Recipient_1,Last_Year_Recipient_2
```

```csv
Alice,alice@example.com,Bob,Charlie
Bob,bob@example.com,Alice,David
Charlie,charlie@example.com,David,Alice
```

4. Ensure the CSV file is in the correct location as specified in `env.py`.

## Usage

1. Run the main script by executing:

   ```bash
   python src/main.py
   ```

2. The script will:
   - Load participant data from the CSV file.
   - Perform the Secret Santa draw based on the configuration (1 or 2 recipients).
   - Send an email to each participant with the names of their gift recipients.
   - Save the updated draw results back to the CSV file.

3. If any errors occur, they will be displayed in the console, and you can retry or debug as needed.

## Customization

- **Number of recipients**: Modify `DRAW_PER_PERSON` in `env.py` to choose whether participants receive one or two recipients.
- **Email content**: Customize the email subject and body in `env.py` using placeholders like `{name}` for the participant's name and `{draws}` for their recipients.
- **CSV file location**: Adjust the `CSV_FILE_PATH` in `env.py` if you prefer a different directory for the participant data.

## File Descriptions

- **`draw.py`**: Contains the logic for performing the Secret Santa draw, ensuring no repeat recipients from last year.
- **`emailer.py`**: Handles email sending via the SMTP server.
- **`file_io.py`**: Responsible for reading and writing the participant data from/to the CSV file.
- **`main.py`**: The main program that ties everything together and coordinates the draw and email sending.
- **`utils.py`**: Utility functions, such as fetching the current date and time.

## Notes

- The project assumes an SMTP server that does not require authentication. If authentication is needed, the script can be extended to support login.
- The project should be run once per year before the holiday season.
- Manually update the CSV file each year with any new participants.

## License

This project is licensed under the MIT License. You are free to modify and distribute the script as needed.

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests to improve this project.
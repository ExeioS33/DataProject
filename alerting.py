import logging
import os
from financial_package.postgres_utils import  DataExporter
from config import DB_CONFIG, TICKERS, SAVE_EXCEL, EMAIL_CONFIG
import smtplib
from email.message import EmailMessage


# Setup logging
log_directory = os.path.abspath("logs")
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, "alerting.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file_path,
    filemode='w'  # Overwrite the log file every time the script runs
)

def send_email_with_attachment(subject: str, body: str, filename: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_CONFIG['sender_email']
    msg['To'] = EMAIL_CONFIG['receiver_email']
    msg.set_content(body)

    with open(filename, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(filename)

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    try:
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['smtp_user'], EMAIL_CONFIG['smtp_password'])
            server.send_message(msg)
            logging.info(f"Email sent to {EMAIL_CONFIG['receiver_email']} with attachment {file_name}.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def main():
    logging.info("Starting the intraday data export process.")

    exporter = DataExporter(
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        save_path=SAVE_EXCEL
    )
    exporter.connect()
    exporter.export_all_tables(TICKERS)
    exporter.close()
    logging.info("Intraday data export completed.")

    excel_filepath = os.path.join(SAVE_EXCEL, "Today_Data.xlsx")
    send_email_with_attachment(
        subject="Intraday Stock Data",
        body="Please find the attached Excel file with today's intraday stock data.",
        filename=excel_filepath
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Error in intraday data export: {e}", exc_info=True)


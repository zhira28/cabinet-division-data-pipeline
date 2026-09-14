from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

from scraper import scrape_policies
from database import MongoDB
from downloader import download_pdf
from pdf_converter import convert_pdf_to_markdown


def scrape_and_save_task():

    policies = scrape_policies()

    print(f"Found {len(policies)} policies")

    db = MongoDB()

    try:

        for policy in policies:

            print(policy)

            db.insert_document(policy)

    finally:

        db.close()


def download_task():

    db = MongoDB()

    try:

        # Get all policies from MongoDB
        policies = db.collection.find({})

        for policy in policies:

            sr_no = policy["sr_no"]
            title = policy["title"]
            pdf_url = policy.get("pdf_url")

            print(
                f"Processing PDF for SR.NO {sr_no}: {title}"
            )

            pdf_path = download_pdf(
                pdf_url,
                sr_no,
                title
            )

            if pdf_path:

                print(
                    f"PDF downloaded successfully: {pdf_path}"
                )

    finally:

        db.close()


def convert_task():

    db = MongoDB()

    try:

        policies = db.collection.find({})

        for policy in policies:

            sr_no = policy["sr_no"]
            title = policy["title"]

            # Re-create PDF path
            filename = f"{sr_no}_{title}.pdf"

            for character in [
                "/", "\\", ":", "*",
                "?", '"', "<", ">", "|"
            ]:
                filename = filename.replace(
                    character,
                    "_"
                )

            pdf_path = f"data/pdfs/{filename}"

            print(
                f"Converting SR.NO {sr_no}: {pdf_path}"
            )

            markdown_path = convert_pdf_to_markdown(
                pdf_path
            )

            if markdown_path:

                print(
                    f"Markdown created: {markdown_path}"
                )

                db.update_document(
                    sr_no,
                    pdf_path,
                    markdown_path
                )

    finally:

        db.close()


with DAG(
    dag_id="cabinet_division_pipeline",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
) as dag:

    scrape = PythonOperator(
        task_id="scrape_policies",
        python_callable=scrape_and_save_task,
    )

    download = PythonOperator(
        task_id="download_pdfs",
        python_callable=download_task,
    )

    convert = PythonOperator(
        task_id="convert_pdfs_to_markdown",
        python_callable=convert_task,
    )

    scrape >> download >> convert
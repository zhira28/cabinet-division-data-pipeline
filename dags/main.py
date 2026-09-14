
from scraper import scrape_policies
from downloader import download_pdf
from pdf_converter import convert_pdf_to_markdown

from database import MongoDB


def main():

    print("Starting Cabinet Division pipeline...")

    # -----------------------------------------
    # 1. Scrape website
    # -----------------------------------------

    policies = scrape_policies()

    print(
        f"Found {len(policies)} policies."
    )

    # -----------------------------------------
    # 2. Connect to MongoDB
    # -----------------------------------------

    db = MongoDB()

    # -----------------------------------------
    # 3. Process policies
    # -----------------------------------------

    for policy in policies:

        sr_no = policy["sr_no"]
        title = policy["title"]

        print(
            f"\nProcessing SR.NO {sr_no}: {title}"
        )

        # -------------------------------------
        # Save metadata FIRST
        # -------------------------------------

        db.insert_document(policy)

        # -------------------------------------
        # Download PDF
        # -------------------------------------

        pdf_path = download_pdf(
            policy["pdf_url"],
            sr_no,
            title
        )

        # -------------------------------------
        # Convert PDF
        # -------------------------------------

        if pdf_path:

            markdown_path = (
                convert_pdf_to_markdown(
                    pdf_path
                )
            )

            # ---------------------------------
            # Update MongoDB
            # ---------------------------------

            if markdown_path:

                db.update_document(
                    sr_no,
                    pdf_path,
                    markdown_path
                )

    # -----------------------------------------
    # 4. Close MongoDB
    # -----------------------------------------

    db.close()

    print(
        "\nPipeline completed successfully!"
    )


if __name__ == "__main__":
    main()


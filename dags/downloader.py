
import os
import requests


PDF_FOLDER = "data/pdfs"


def download_pdf(pdf_url, sr_no, title):

    if not pdf_url:
        print(f"No PDF URL: {title}")
        return None

    os.makedirs(
        PDF_FOLDER,
        exist_ok=True
    )

    # Create filename
    filename = f"{sr_no}_{title}.pdf"

    # Remove unsafe filename characters
    for character in [
        "/", "\\", ":", "*",
        "?", '"', "<", ">", "|"
    ]:
        filename = filename.replace(
            character,
            "_"
        )

    file_path = os.path.join(
        PDF_FOLDER,
        filename
    )

    try:

        print(
            f"Downloading: {title}"
        )

        response = requests.get(
            pdf_url,
            timeout=30
        )

        response.raise_for_status()

        # Make sure we received a PDF
        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        if (
            "pdf" not in content_type.lower()
            and not pdf_url.lower().endswith(".pdf")
        ):
            print(
                f"ERROR: URL did not return a PDF: "
                f"{pdf_url}"
            )

            return None

        # Save PDF
        with open(
            file_path,
            "wb"
        ) as file:

            file.write(
                response.content
            )

        print(
            f"Downloaded: {file_path}"
        )

        return file_path

    except requests.RequestException as error:

        print(
            f"Download failed: {title}"
        )

        print(error)

        return None


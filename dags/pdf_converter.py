import os
import pymupdf4llm


PDF_FOLDER = "data/pdfs"
MARKDOWN_FOLDER = "data/markdown"


def convert_pdf_to_markdown(pdf_path):

    # Create markdown folder
    os.makedirs(
        MARKDOWN_FOLDER,
        exist_ok=True
    )

    # Get PDF filename without extension
    filename = os.path.basename(pdf_path)

    name = os.path.splitext(filename)[0]

    # Create Markdown file path
    markdown_path = os.path.join(
        MARKDOWN_FOLDER,
        name + ".md"
    )

    try:

        print(f"Converting: {filename}")

        # Convert PDF to Markdown
        markdown_text = pymupdf4llm.to_markdown(
            pdf_path
        )

        # Save Markdown file
        with open(
            markdown_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(markdown_text)

        print(
            f"Markdown created: {markdown_path}"
        )

        return markdown_path

    except Exception as error:

        print(
            f"Error converting {filename}: {error}"
        )

        return None



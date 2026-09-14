
import os
from pathlib import Path

from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# ---------------------------------------------------------
# Website configuration
# ---------------------------------------------------------

SOURCE_URL = os.getenv(
    "SOURCE_URL",
    "https://cabinet.gov.pk/Policies"
)


# ---------------------------------------------------------
# MongoDB configuration
# ---------------------------------------------------------

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

MONGO_DATABASE = os.getenv(
    "MONGO_DATABASE",
    "cabinet_division"
)

MONGO_COLLECTION = os.getenv(
    "MONGO_COLLECTION",
    "documents"
)


# ---------------------------------------------------------
# Directory configuration
# ---------------------------------------------------------

PDF_DIRECTORY = Path(
    os.getenv("PDF_DIRECTORY", "data/pdfs")
)

MARKDOWN_DIRECTORY = Path(
    os.getenv("MARKDOWN_DIRECTORY", "data/markdown")
)


# ---------------------------------------------------------
# HTTP configuration
# ---------------------------------------------------------

REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", "30")
)

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", "3")
)


# ---------------------------------------------------------
# Create required directories
# ---------------------------------------------------------

PDF_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

MARKDOWN_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


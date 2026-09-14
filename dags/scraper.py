
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://cabinet.gov.pk"
POLICIES_URL = f"{BASE_URL}/Policies"


def scrape_policies():

    print("Opening Policies page...")

    # -----------------------------------------
    # 1. Open Policies page
    # -----------------------------------------

    response = requests.get(
        POLICIES_URL,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    policies = []

    # Find all tables
    tables = soup.find_all("table")

    for table in tables:

        rows = table.find_all("tr")

        for row in rows:

            columns = row.find_all("td")

            # Skip header/invalid rows
            if len(columns) < 3:
                continue

            # -----------------------------------------
            # Get basic information
            # -----------------------------------------

            sr_no = columns[0].get_text(
                strip=True
            )
            # print(f"Found row: SR.NO={sr_no}")

            title = columns[1].get_text(
                " ",
                strip=True
            )

            date = columns[2].get_text(
                " ",
                strip=True
            )

            # -----------------------------------------
            # Get PolicyDetail URL
            # -----------------------------------------

            detail_link = row.find(
                "a",
                href=True
            )

            if not detail_link:
                print(
                    f"No detail link found: {title}"
                )
                continue

            detail_url = urljoin(
                BASE_URL,
                detail_link["href"]
            )

            print(
                f"\nProcessing: {title}"
            )

            print(
                f"Detail URL: {detail_url}"
            )

            # -----------------------------------------
            # 2. Open PolicyDetail page
            # -----------------------------------------

            try:

                detail_response = requests.get(
                    detail_url,
                    timeout=30
                )

                detail_response.raise_for_status()

            except requests.RequestException as error:

                print(
                    f"Could not open detail page: {error}"
                )

                continue

            # -----------------------------------------
            # 3. Find actual PDF link
            # -----------------------------------------

            detail_soup = BeautifulSoup(
                detail_response.text,
                "html.parser"
            )

            pdf_url = None

            # Look through all links on detail page
            for link in detail_soup.find_all(
                "a",
                href=True
            ):

                href = link["href"]

                # Actual PDF links contain .pdf
                if ".pdf" in href.lower():

                    pdf_url = urljoin(
                        BASE_URL,
                        href
                    )

                    break

            # -----------------------------------------
            # 4. Check if PDF was found
            # -----------------------------------------

            if pdf_url:

                print(
                    f"PDF URL: {pdf_url}"
                )

            else:

                print(
                    f"PDF not found: {title}"
                )

            # -----------------------------------------
            # 5. Store record
            # -----------------------------------------

            policy = {
                "sr_no": sr_no,
                "title": title,
                "date": date,
                "pdf_url": pdf_url
            }

            policies.append(policy)

    print(
        f"\nTotal policies found: {len(policies)}"
    )

    return policies


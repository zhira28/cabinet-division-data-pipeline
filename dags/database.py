
from pymongo import MongoClient


class MongoDB:

    def __init__(self):

        self.client = MongoClient(
            "mongodb://host.docker.internal:27017/"
        )

        self.db = self.client["cabinet_division_db"]

        self.collection = self.db["policies"]

    def insert_document(self, policy):

        try:

            result = self.collection.update_one(

                # Use SR.NO as unique identifier
                {
                    "sr_no": policy["sr_no"]
                },

                # Insert/update document
                {
                    "$set": policy
                },

                # Create document if it doesn't exist
                upsert=True
            )

            print(
                f"MongoDB saved: SR.NO {policy['sr_no']}"
            )

        except Exception as error:

            print(
                f"MongoDB insert error for "
                f"SR.NO {policy['sr_no']}: {error}"
            )

    def update_document(
        self,
        sr_no,
        pdf_path,
        markdown_path
    ):

        try:

            result = self.collection.update_one(

                {
                    "sr_no": sr_no
                },

                {
                    "$set": {
                        "pdf_path": str(pdf_path),
                        "markdown_path": str(markdown_path),
                        "downloaded": True,
                        "converted_to_markdown": True
                    }
                }
            )

            if result.matched_count == 0:

                print(
                    f"Warning: SR.NO {sr_no} "
                    f"not found in MongoDB"
                )

        except Exception as error:

            print(
                f"MongoDB update error for "
                f"SR.NO {sr_no}: {error}"
            )

    def close(self):

        self.client.close()


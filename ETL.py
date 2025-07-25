
import os
import requests
from requests.auth import HTTPBasicAuth
import json
from typing import Any

from dotenv import load_dotenv
load_dotenv()

class ETLPipeline:
    def extract(self) -> Any:
        """
        Extract data from source(s).
        Returns:
            Extracted data (e.g., DataFrame, list, etc.)
        """
        ONET_API_URL = "https://services.onetcenter.org/ws/online/search"

        username = os.getenv("ONET_API_USERNAME")
        password = os.getenv("ONET_API_PASSWORD")

        job_title = "Software Engineer"  # Hardcoded for now, or use input()
        headers = {"Accept": "application/json"}
        params = {"keyword": job_title}
        print(f"Requesting: {ONET_API_URL} with params: {params}")
        response = requests.get(
            ONET_API_URL,
            auth=HTTPBasicAuth(username, password),
            headers=headers,
            params=params
        )
        print(response.status_code)

        if response.status_code == 200:
            response_data = response.json()
            if response_data:
                with open("output.json", "w") as f:
                    json.dump(response_data, f, indent=4)
            else:
                print("Error:", response.status_code, response.text)
                return None

    def transform(self, data: Any) -> Any:
        """
        Transform the extracted data.
        Args:
            data: The data extracted from the source
        Returns:
            Transformed data
        """
        # TODO: Implement transformation logic
        pass

    def load(self, data: Any) -> None:
        """
        Load the transformed data to the destination.
        Args:
            data: The transformed data
        """
        # TODO: Implement loading logic
        pass

    def run(self):
        """
        Run the ETL pipeline: extract, transform, and load.
        """
        data = self.extract()
        print(data)
        data = self.transform(data)
        self.load(data)


if __name__ == "__main__":
    etl = ETLPipeline()
    etl.run()

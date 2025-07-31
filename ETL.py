
import os
import requests
from requests.auth import HTTPBasicAuth
import json
from typing import Any

from dotenv import load_dotenv

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
                relevent_occupations = ExtractOccupation(response_data, 
                                                         username=username, 
                                                         password=password, 
                                                         headers=headers,)
                with open('output.json', 'w') as f:
                    json.dump(relevent_occupations, f, indent=4)
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

def ExtractOccupation(response_data, username, password, headers):
    # TODO: Implement logic to extract each occupation
    occupations_list = []
    
    for each_occupations in response_data["occupation"]:
        print(f"Requesting: {each_occupations['href']} for occupation: {each_occupations['title']}")
        this_occupation_response = requests.get(            
            each_occupations["href"],
            auth=HTTPBasicAuth(username, password),
            headers=headers
        )
        if this_occupation_response.status_code == 200:
            occupation_data = this_occupation_response.json()
            occupations_list.append(occupation_data)
        else:            
            print(f"Error fetching occupation {each_occupations['title']}: {this_occupation_response.status_code} - {this_occupation_response.text}")

    return occupations_list  # Return the list of occupations or process as needed

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    etl = ETLPipeline()
    etl.run()

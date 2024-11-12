
import json
import re
import requests
from typing import List, Tuple, Generator, Optional
from pydantic import BaseModel, constr, Field

# Pydantic model for message structure validation
class Message(BaseModel):
    role: str = Field(..., pattern=r"^(user|assistant)$")  #   # Role should be either 'user' or 'assistant'
    content: str  # Content of the message


def call_model(messages: List[Message], endpoint_name: str, token: str) -> dict:
    """
    Sends a list of messages to the Databricks model endpoint and returns the response.
    
    Args:
        messages (List[Message]): List of messages with role and content to be sent to the model.
    
    Returns:
        dict: The JSON response from the Databricks endpoint.
    """
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}  # Set headers
    ds_dict = {'messages': messages, 'databricks_options': {'return_trace': True}}  # Prepare payload
    data_json = json.dumps(ds_dict, allow_nan=True)  # Serialize data to JSON
    response = requests.request(method='POST', headers=headers, url=endpoint_name, data=data_json)  # Send POST request
    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')  # Raise exception on failure
    return response.json()  # Return the response JSON

def call_model_stream(messages: List[Message], endpoint_name: str, token: str) -> Generator[str, None, None]:
    """
    Sends a list of messages to the Databricks model endpoint and streams the response chunks.
    
    Args:
        messages (List[Message]): List of messages with role and content to be sent to the model.
    Yields:
        str: Chunks of the response content.
    """
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}  # Set headers
    ds_dict = {'stream': True, 'messages': messages, 'databricks_options': {'return_trace': True}}  # Prepare payload
    data_json = json.dumps(ds_dict, allow_nan=True)  # Serialize data to JSON
    response = requests.post(url=endpoint_name, headers=headers, data=data_json, stream=True)  # Send streaming POST request

    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')  # Raise exception on failure

    # Yield chunks of the response as they are received
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            yield chunk.decode('utf-8')  # Decode and yield each chunk

def parse_chunk(chunk: str) -> Optional[str]:
    """
    Parses a chunk of response data and extracts the content.
    
    Args:
        chunk (str): A chunk of the response data.
    
    Returns:
        Optional[str]: The content of the chunk if available, else None.
    """
    chunk_str = chunk.strip().lstrip('data:').strip()  # Clean the chunk string
    
    try:
        if "choices" in chunk_str:
            chunk_data = json.loads(chunk_str)  # Parse the chunk as JSON
            if chunk_data["choices"]:
                delta = chunk_data["choices"][0].get("delta", {})
                content = delta.get("content", None)  # Extract content from delta
                if content:
                    return content
    except json.JSONDecodeError:
        return None  # Return None if JSON decoding fails
    return None


def extract_databricks_output(string: str) -> Optional[dict]:
    """
    Extracts the 'databricks_output' from a given string using regex.
    
    Args:
        string (str): The input string containing Databricks output.
    
    Returns:
        Optional[dict]: The extracted Databricks output as a JSON object, or None if extraction fails.
    """
    pattern = r'"databricks_output":\s*({.*?})\s*data:\s*\[DONE'  # Regex pattern to extract output
    match = re.search(pattern, string, re.DOTALL)  # Search for pattern in the string
    if match:
        databricks_output_str = match.group(1)[:-1]  # Get matched output
        try:
            databricks_output_json = json.loads(databricks_output_str)  # Convert to JSON
            return databricks_output_json
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No 'databricks_output' found in the string.")
        return None


def generate_reference_section(response: dict) -> Tuple[str, List[str]]:
    """
    Generates the reference section from the response's trace data.
    
    Args:
        response (dict): The model response containing trace data.
    
    Returns:
        str: The formatted reference section as HTML.
    """
    
    
    references = ""
    urls = []    
    for item in response['trace']['data']['spans']:
        if item['name'] == 'VectorStoreRetriever':
            string_references = json.loads(item['attributes']['mlflow.spanOutputs'])  # Extract reference data

            count = 1
            for ref in string_references:
                
                url = ref['metadata']['url'][1:] if ref['metadata']['url'].startswith('/') else ref['metadata']['url']
                
                urls.append(url)
                references += f"""**{count}. {url}** <br />
                                {ref['page_content']} <br />
                            """
                count += 1
            
            return references, urls
    
    return "", []


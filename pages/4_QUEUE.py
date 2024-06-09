import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize boto3 client for SQS with hardcoded credentials
def get_sqs_client():
    try:
        sqs = boto3.client(
            'sqs',
            aws_access_key_id="",
            aws_secret_access_key="",
            aws_session_token="",
            region_name='us-east-1'
        )
        return sqs
    except NoCredentialsError:
        st.error("AWS credentials not found.")
        return None
    except PartialCredentialsError:
        st.error("Incomplete AWS credentials.")
        return None

# List all queues and their message counts
def list_queues(sqs):
    try:
        response = sqs.list_queues()
        queue_urls = response.get('QueueUrls', [])
        queue_data = []
        for url in queue_urls:
            queue_name = url.split('/')[-1]
            attributes = sqs.get_queue_attributes(QueueUrl=url, AttributeNames=['ApproximateNumberOfMessages'])
            message_count = attributes['Attributes']['ApproximateNumberOfMessages']
            queue_data.append({'Queue Name': queue_name, 'Message Count': message_count})
        return queue_data
    except Exception as e:
        st.error(f"Error listing queues: {e}")
        return []

def main():
    st.title("AWS SQS Queue Viewer")

    sqs = get_sqs_client()
    if sqs is None:
        return

    queue_data = list_queues(sqs)
    if not queue_data:
        st.write("No queues available.")
        return

    st.table(queue_data)

if __name__ == "__main__":
    main()

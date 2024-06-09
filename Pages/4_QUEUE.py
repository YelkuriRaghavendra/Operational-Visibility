import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Initialize boto3 client for SQS with hardcoded credentials
def get_sqs_client():
    try:
        sqs = boto3.client(
            'sqs',
            aws_access_key_id="ASIA3FLDYIYZJOYBGDMT",
            aws_secret_access_key="lKDm8ncg3fiSxehjNQUACQARYMiXw3EFoPK//g8m",
            aws_session_token="IQoJb3JpZ2luX2VjEJT//////////wEaCXVzLWVhc3QtMSJHMEUCICHTkw4mkz6IyavKEgVWj+VKy6rFbBMsU+NVGGpO6x6hAiEA5g4CM7Hq6vqC8LUdms5kxbpJIKopHpiSvI0aTHCoTVgqoAMILBAAGgw3NjczOTc3NDIxMzAiDFDVmlTFuuI2ZUnTrSr9ApEF8GF1IUHpUglxh4QcJT12D5bCt4gooR8YZoFNPfd/hO31Mf9pS8ff1494lE6oohIIPtRGr6jS2vjYnHRq74sMgQ7Yd6C73EAR1JINI0ghUC7/4DLGUvIsMecQwzMGkb1zzvBrTToeJTUSrAx7laZ0mz+1cqDnxRf5DGAYcWb2SU5CZPAZY6eVTKXRZwByVufh2o07z9VgLCgKlEvjuOsGgDseilWFD08Zkj0gBNTBmq9yQNcd/zDWqK0RHWIVVsD5oNPaQMsreG1XbnMl431csv57hjKsAF8ozA6CKzXett4UGT1QyHa15Nb2FMIS2OLWpq3bdImYJWH97Zsn0dfWcNGtwRFI80hdM5mhAchfCUqadMyBZOPVo7tVotPcaeqwVFbDRo/gH37d00x6a228v7jeBRDf99NLO0sjeq2HYraIIpzgYEsN1APsH5kWMEB2Fwf5ixr3ZD+gXWHsRxDtMQmxpvHzCkQcIWJH9sHdyKaKt4XsoLWjUCrmPDCmm5azBjqmAf2KbrJt69gRn1ABMxrlnAOgmEUA78nuoQsGlM5n2pZ35jms1lJO5zapzNK+WUhITHbASNW4ds8CIetXGBIC1I9uutkQEZ+JBGW18sugCkwbhy+FJr4s04ZO2KUrAG6BQXRUU4J0k5m32bHWL/aWzx1RsxuN2j1a570PIy9D9D+9w5tRGvUxwwjo0JfspZB6TUgk5USP632HA8+yYwqsvOLsFfRMaMQ=",
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

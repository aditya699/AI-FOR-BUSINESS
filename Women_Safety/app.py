#Import Libary
import streamlit as st
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

#Function to hit the endpoint and get result
def analyze_text(text1,senstivity):
    #Not a safe a practice to expose your key and endpoint this is just for poc purpose
    # analyze text
    key = 'cec3bcaab47e42b195dc9076e8edcd61'
    endpoint = 'https://contentsafetyaditya.cognitiveservices.azure.com/'

    # Create an Azure AI Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Contruct request
    request = AnalyzeTextOptions(text=text1)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise

    hate=list(response['categoriesAnalysis'][0].values())[1]
    selfharm=list(response['categoriesAnalysis'][1].values())[1]
    sexual=list(response['categoriesAnalysis'][2].values())[1]
    violence=list(response['categoriesAnalysis'][3].values())[1]

    if hate or selfharm or sexual or violence >=senstivity:
        return f"As per our assesment this comment voilates the safety guidelines set up by our company, Thanks for reporting this comment will be reomved in next 24 hrs"


    else:
        return f"No Issues Found!!!!"
    
def main(senstivity):
    st.title("Instamart")

    # Display a static image
    st.image("pic.jpeg", caption="My Image", width=300)

    # Comments Section
    st.header("Comments Section")

    # Get comments from user
    user_comment = st.text_area("Add your comment:")

    # Report Button for each comment
    if st.button("Report Comment"):
        # Call your analyze_text function here
        categories = analyze_text(user_comment,senstivity)

        
        st.success(f"{categories}")

if __name__ == '__main__':
    main(2)
from github import Github
from dotenv import load_dotenv
import os

load_dotenv(override=True)

ACCESS_TOKEN = os.environ['GH_ACCESS_TOKEN'] 
REPO_NAME = 'johnnyeats'

def create_issue(title, body):
    try:
        g = Github(ACCESS_TOKEN)
        repo = g.get_user().get_repo(REPO_NAME)
        repo.create_issue(title=title, body=body)
        print("Issue created successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
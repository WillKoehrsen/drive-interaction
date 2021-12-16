## Obsolete file to get all folders within Audiobook folder
## Not able to get size of folders

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pandas as pd


def get_audiobook_folder_contents():
    """
    Retrieves the contents of the Audiobooks folder. Retrieves each top level directory
    within the Audiobook folder but not detailed info about the files in directories.
    """
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    creds = None

    # token.pickle stores the user's access and refresh tokens and is automatically created
    # when the authorization flow completes for the first time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # Refresh the creds if they have just expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # Create new credentials based on the user's credentials and desired scopes
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)

    # List audiobook folders
    audiobook_folders = (
        service.files()
        .list(q="name='Audiobooks' and mimeType = 'application/vnd.google-apps.folder'")
        .execute()
    )

    import pprint

    pprint.pprint(f"Audiobook folders: {audiobook_folders}")

    # Hardcoded id from looking at folder in drive
    KNOWN_ID_ = "0B_41odSiCNW8aW16TURIM2ZRR2s"

    # Fields to retrieve from the files
    fields = "files(createdTime,name,webViewLink,webContentLink,quotaBytesUsed)"

    books = (
        service.files()
        .list(
            q=f"parents in '{KNOWN_ID_}' and mimeType = 'application/vnd.google-apps.folder'",
            pageSize=1000,
            fields=fields,
        )
        .execute()
    )

    book_df = pd.DataFrame(books["files"])

    if book_df.shape[0] > 999:
        print("Search may be incomplete.")

    book_df.to_csv("top-level-audiobooks.csv", index=False)

    print(f"Book dataframe information:\n{book_df.info()}")

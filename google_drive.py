from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

from werkzeug.utils import secure_filename

import io

#--------------------------------------------------------------------------------------------------

def create_folder(flow):

    creds = flow.credentials

    # creating folder
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        folder_metadata = {
            'name': 'Adverts',
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # pylint: disable=maybe-no-member
        folder = service.files().create(body=folder_metadata,
                                      fields='id' ).execute()
        print(F'Folder ID: "{folder.get("id")}".')
        return folder.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None
    
#--------------------------------------------------------------------------------------------------
    
def upload_to_folder(flow, folder_id, file):

    creds = flow.credentials

    file_name = secure_filename(file.filename)

    try:
    # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        
        f = io.BytesIO(file.read())
        media = MediaIoBaseUpload(f, mimetype='image/jpeg', resumable=True)

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None





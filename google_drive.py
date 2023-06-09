from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

from werkzeug.utils import secure_filename

import io

#--------------------------------------------------------------------------------------------------

folder_name = 'Adverts'

#--------------------------------------------------------------------------------------------------

def folder_there(flow):

    global folder_name

    creds = flow.credentials

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        # pylint: disable=maybe-no-member
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and name='Adverts'",
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        folders = results.get('files', [])

        print(folders)

        if not folders:
            print('No files found.')
            return 0
        
        else:
            print('Folders:')
            for item in folders:
                print(u'{0} ({1})'.format(item['name'], item['id']))
            return folders[0]['id']     # return folder id if present

    except HttpError as error:
        print(F'An error occurred: {error}')
        return 0


#--------------------------------------------------------------------------------------------------

def create_folder(flow):

    global folder_name

    creds = flow.credentials

    folder_id = folder_there(flow)

    if folder_id is not 0:
        print(f"\n\n------------folder present----------{folder_id}------\n\n")
        return folder_id        # return the folder id already present

    # else creating folder
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





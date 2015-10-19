import pprint

import httplib2
import apiclient.discovery
import apiclient.http
import oauth2client.client
from apiclient import errors
from apiclient.http import MediaFileUpload

import magic

# OAuth 2.0 scope that will be authorized.
# Check https://developers.google.com/drive/scopes for all available scopes.
OAUTH2_SCOPE = 'https://www.googleapis.com/auth/drive'

# Location of the client secrets.
CLIENT_SECRETS = 'client_secrets.json'

# Path to the file to upload.
FILENAME = 'document.txt'

# Metadata about the file.
MIMETYPE = 'text/plain'
TITLE = 'My New Text Document'
DESCRIPTION = 'A shiny new text document about hello world.'



def auth():
	# Perform OAuth2.0 authorization flow.
	flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRETS, OAUTH2_SCOPE)
	flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
	authorize_url = flow.step1_get_authorize_url()
	print 'Go to the following link in your browser: ' + authorize_url
	code = raw_input('Enter verification code: ').strip()
	credentials = flow.step2_exchange(code)

	# Create an authorized Drive API client.
	http = httplib2.Http()
	credentials.authorize(http)
	drive_service = apiclient.discovery.build('drive', 'v2', http=http)
	return drive_service

def returnMimeType(locationOfFile): 
	return magic.from_file(locationOfFile, mime=True)

def upload():
	# Insert a file. Files are comprised of contents and metadata.
	# MediaFileUpload abstracts uploading file contents from a file on disk.
	media_body = apiclient.http.MediaFileUpload(
	    FILENAME,
	    mimetype=MIMETYPE,
	    resumable=True
	)
	# The body contains the metadata for the file.
	body = {
	  'title': TITLE,
	  'description': DESCRIPTION,
	}

	# Perform the request and print the result.
	new_file = drive_service.files().insert(body=body, media_body=media_body).execute()
	pprint.pprint(new_file)
	return;


def getID(service, filename):
	# fileID = ""

	# file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
	# for file2 in file_list:
	# 	print 'title: %s, id: %s' % (file2['title'], file2['id'])
	# 	if file2['title'] == filename:
	# 		fileID = file2['id']
	# 		break
	# if fileID == "":
	# 	print 'ERROR: Unable to find `backup` folder.'
	# 	exit()

	# return fileID

	fileID = ""

	result = []
	page_token = None
	while True:
		try:
			param = {}
			param['q'] = "title = '" + filename + "' and 'root' in parents and trashed=false"
			if page_token:
				param['pageToken'] = page_token
			files = service.files().list(**param).execute()

			result.extend(files['items'])

			# print files['items'][0]['title'], files['items'][0]['id']

			fileID = files['items'][0]['id']

			page_token = files.get('nextPageToken')
      			if not page_token:
        			break
    		except errors.HttpError, error:
      			print 'An error occurred: %s' % error
      			break

      	if fileID == "":
      		print 'ERROR: Unable to find `backup` folder.'
		exit()

  	return fileID





def backup(destDir, targetDir):
	# print fileType
	drive = auth()
	backupID = getID(drive, targetDir)

	for root, dirnames, filenames in os.walk(destDir):
		for f in filenames:
			if f.endswith(fileType):
				upload(drive, destDir, backupID, f)
	return;

def retrieve_all_files(service):
	"""Retrieve a list of File resources.

	Args:
		service: Drive API service instance.
	Returns:
		List of File resources.
	"""
	result = []
	page_token = None
	while True:
		try:
			param = {}
			param['q'] = "'root' in parents and trashed=false"
			if page_token:
				param['pageToken'] = page_token
			files = service.files().list(**param).execute()

			result.extend(files['items'])
			page_token = files.get('nextPageToken')
      			if not page_token:
        			break
    		except errors.HttpError, error:
      			print 'An error occurred: %s' % error
      			break
  	return result


def print_files_in_folder(service, folder_id):
	"""Print files belonging to a folder.

	Args:
		service: Drive API service instance.
		folder_id: ID of the folder to print files from.
	"""
	page_token = None
	while True:
		try:
			param = {}
			param['q'] = "trashed=false"
			if page_token:
				param['pageToken'] = page_token
			children = service.children().list(
			  	folderId=folder_id, **param).execute()

			for key in children.get('items', []):
				print '%s: \n\n' % (key)
			page_token = children.get('nextPageToken')
			if not page_token:
				break
		except errors.HttpError, error:
			print 'An error occurred: %s' % error
			break


def insert_file(service, title, description, parent_id, mime_type, filename):
	"""Insert new file.

	Args:
		service: Drive API service instance.
		title: Title of the file to insert, including the extension.
		description: Description of the file to insert.
		parent_id: Parent folder's ID.
		mime_type: MIME type of the file to insert.
		filename: Filename of the file to insert.
	Returns:
		Inserted file metadata if successful, None otherwise.
	"""
	media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
	body = {
		'title': title,
		'description': description,
		'mimeType': mime_type
	}
	# Set the parent folder.
	if parent_id:
		body['parents'] = [{'id': parent_id}]

	try:
		file = service.files().insert(
			body=body,
		        media_body=media_body
		        ).execute()

	# Uncomment the following line to print the File ID
	# print 'File ID: %s' % file['id']

		return file
	except errors.HttpError, error:
		print 'An error occured: %s' % error
	return None



# print returnMimeType("../backup/crawl.zip")
drive_service = auth()

f = open("log.txt", "w")
lists = retrieve_all_files(drive_service)
# print lists[1]
for items in lists:
	# print type(items)
	for key, val in items.items():
		f.write('%s: %s\n' % (key, val))
		# print key, val
		# print type(item)

	f.write('\n')

print_files_in_folder(drive_service, "0B6VQvaBr5t02UFJCWklGM3dIU00")
f.close()

getID(drive_service, "backup")

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

import pprint

import httplib2
import apiclient.discovery
import apiclient.http
import oauth2client.client

from apiclient import errors


def auth():
	gauth = GoogleAuth()
	gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication

	# print type(code)

	code = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance

	
	return code



def uploadFolder(parentID, folderTitle):
	createFolder(parentID, folderTitle)

	return;


def createFolder(parentID, folderTitle):

	return;


def upload(currentDir):
	# infos = []
	for files in os.walk(currentDir): # Walk directory tree
		for f in files:
			# if os.path.isdir()
			# print f[3] + ", " + os.path.is
			print f
	return;

def tt(drive):
	backupID = ""

	file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
	for file2 in file_list:
		print 'title: %s, id: %s' % (file2['title'], file2['id'])
		if file2['title'] == "backup":
			backupID = file2['id']
	if backupID == "":
		print 'ERROR: Unable to find `backup` folder.'
		exit()

	# file1 = drive.CreateFile({'title': "ttt", 
	# 	"parents": [{"kind": "drive#fileLink","id": backupID}],
	# 	"mimeType": "application/vnd.google-apps.folder"}) # Create GoogleDriveFile instance with title 'Hello.txt'
	# # file1.SetContentString('{"firstname": "John", "lastname": "Smith"}')
	# # file1.SetContentFile('document.txt')
	# file1.Upload() # Upload it
	# print 'title: %s, id: %s' % (file1['title'], file1['id']) # title: Hello.txt, id: {{FILE_ID}}

	## backupID: 0B6VQvaBr5t02UFJCWklGM3dIU00

	## tttID: 0ByNEvMYj64ZeLW9SYWhjNDI2VFU

	for file_list in drive.ListFile({'q': "'" + backupID + "' in parents and trashed=false"}):
		for file2 in file_list:
			print 'title: %s, id: %s' % (file2['title'], file2['id'])
			if file2['title'] == "ttt":
				print file2['id']
				print "dasdasfsgdfgsdfgsdfg"
				# file3 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": file2['id']}]})
				# file3.SetContentFile('document.txt')
				# file3.Upload() # Update metadata

	return;


def test(drive):
	# file1 = drive.CreateFile({'parent': [{
	# 	"kind": "drive#fileLink",
	# 	"id": "0ByNEvMYj64ZeLW9SYWhjNDI2VFU"
	# 	}]})
	# file1.SetContentFile('test.txt')
	children = drive.children.list()
	print "mnbvc"
	return;

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
			if page_token:
				param['pageToken'] = page_token
			children = service.children().list(
				folderId=folder_id, **param).execute()

			for child in children.get('items', []):
				print 'File Id: %s' % child['id']
			page_token = children.get('nextPageToken')
			if not page_token:
				break
		except errors.HttpError, error:
			print 'An error occurred: %s' % error
			break


def authClient(code):
	credentials = flow.step2_exchange(code)
	# Create an authorized Drive API client.
	http = httplib2.Http()
	credentials.authorize(http)
	drive_service = apiclient.discovery.build('drive', 'v2', http=http)
	return;
 	
drive = auth()
# test(drive)
print_files_in_folder(drive, "0ByNEvMYj64ZeLW9SYWhjNDI2VFU")
# upload("../crawl")

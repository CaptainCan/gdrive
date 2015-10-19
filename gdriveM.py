from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def auth():
	gauth = GoogleAuth()
	gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication

	# print type(code)

	drive = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance
	
	return drive

def getID(drive, targetDir):
	backupID = ""

	file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
	for file2 in file_list:
		print 'title: %s, id: %s' % (file2['title'], file2['id'])
		if file2['title'] == targetDir:
			backupID = file2['id']
			break
	if backupID == "":
		print 'ERROR: Unable to find `backup` folder.'
		exit()

	return backupID

def upload(drive, destDir, backupID, filename):

	if exists(drive, backupID, filename):
		print filename + " exists\n"
		return
	else:
		file1 = drive.CreateFile({ 
			"parents": [{"kind": "drive#fileLink","id": backupID}]
			}) # Create GoogleDriveFile instance with title 'Hello.txt'
		# file1.SetContentString('{"firstname": "John", "lastname": "Smith"}')
		file1.SetContentFile(filename)
		file1.Upload() # Upload it
		print 'Uploaded title: %s, id: %s' % (file1['title'], file1['id']) # title: Hello.txt, id: {{FILE_ID}}

		return;


def exists(drive, backupID, filename):
	for file_list in drive.ListFile({'q': "'" + backupID + "' in parents and trashed=false"}):
		for file2 in file_list:
			# print 'title: %s, id: %s' % (file2['title'], file2['id'])
			if file2['title'] == filename:
				return True
	return False


def backup(destDir, targetDir):
	# print fileType
	drive = auth()
	backupID = getID(drive, targetDir)

	for root, dirnames, filenames in os.walk(destDir):
		for f in filenames:
			if f.endswith(fileType):
				upload(drive, destDir, backupID, f)
	return;

fileType = ".zip"
# drive = auth()
backup(".", "backup")


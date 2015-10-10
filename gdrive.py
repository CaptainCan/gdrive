# from oauth2client import client

# flow = client.flow_from_clientsecrets(
#     'client_secrets.json',
#     scope='https://www.googleapis.com/auth/drive.metadata.readonly',
#     redirect_uri='http://www.example.com/oauth2callback')


import pprint

import httplib2
import apiclient.discovery
import apiclient.http
import oauth2client.client

flow = oauth2client.client.flow_from_clientsecrets(
	'client_secrets.json',
    	scope='https://www.googleapis.com/auth/drive'
)
flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
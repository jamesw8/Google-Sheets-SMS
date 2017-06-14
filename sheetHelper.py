from googleapiclient import discovery

import httplib2
from oauth2client import tools, client
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError, OAuth2WebServerFlow

import simplejson as json

CLIENT_SECRET_FILE = 'client_secret.json'
scope = 'https://www.googleapis.com/auth/spreadsheets'

storage = Storage('sheets.storage')
flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scope)
flow.user_agent = "Sheetspread"
credentials = storage.get()
if credentials is None:
	credentials = tools.run_flow(flow, storage)

http = credentials.authorize(httplib2.Http())

service = discovery.build('sheets', 'v4', http=http)

s = open('spreadsheet', 'r')
spreadsheet = s.read().split()[0]

_range = "Sheet1!B:B"
retSheet = service.spreadsheets().values().get(
		spreadsheetId=spreadsheet,
		range=_range).execute()

def updateSheet():
	global retSheet
	retSheet = service.spreadsheets().values().get(
		spreadsheetId=spreadsheet,
		range=_range).execute()
	return retSheet

def addToSheet(addInput):
	valueCount = len(retSheet['values'])
	print("Proceeding to add", addInput)
	value = [ [addInput] ]
	body = { 'values': value }

	_range = "Sheet1!B" + str(valueCount+1) + ":B"
	service.spreadsheets().values().update(
		spreadsheetId=spreadsheet,
		range=_range,
		body = body,
		valueInputOption="RAW"
		).execute()

def delFromSheet(delInput):
	values = retSheet['values']
	d

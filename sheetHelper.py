from googleapiclient import discovery

import httplib2
from oauth2client import tools, client
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError, OAuth2WebServerFlow

import simplejson as json

import os

CLIENT_SECRET_FILE = 'client_secret.json'
scope = 'https://www.googleapis.com/auth/spreadsheets'
try:
	storage = Storage('sheets.storage')
	flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scope)
	flow.user_agent = "Sheetspread"
	flow.params['access_type'] = 'offline'
	credentials = storage.get()
	if credentials is None or credentials.invalid:
		credentials = tools.run_flow(flow, storage)
except:
	credentials = client.OAuth2Credentials(
		os.environ.get("access_token"),
		os.environ.get("client_id"),
		os.environ.get("client_secret"),
		os.environ.get("refresh_token"),
		os.environ.get("token_expiry"),
		os.environ.get("token_uri"),
		"Sheetspread",
		scopes=[scope])

http = credentials.authorize(httplib2.Http())

service = discovery.build('sheets', 'v4', http=http)
try:
	s = open('spreadsheet', 'r')
	spreadsheet = s.read().split()[0]
except:
	spreadsheet = os.environ.get("spreadsheet_id")

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
	success = True
	try:
		del values[delInput]
		valueCount = len(values)
		_range="Sheet1!B" + str(delInput+1) + ":B"
		value = []
		for v in values[delInput:]:
			value.append(v)
		value.append([''])
		body = { 'values': value }

		service.spreadsheets().values().update(
			spreadsheetId=spreadsheet,
			range=_range,
			body = body,
			valueInputOption="RAW"
			).execute()
		print(valueCount)
		print(values)
	except IndexError:
		success = False
	return success
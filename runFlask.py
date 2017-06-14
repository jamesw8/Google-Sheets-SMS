from flask import Flask, request, render_template
from twilio.rest import Client
import requests
import sheetHelper
app = Flask(__name__)

f = open('twilioapi', 'r')
n = open('numbers', 'r')
acc = f.read().split()
num = n.read().split()
ACCOUNT_SID = acc[0]
AUTH_TOKEN = acc[1]
NUMBER1 = num[0]
NUMBER2 = num[1]
NUMBER3 = num[2]
f.close()
n.close()

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/')
def index():
	return 'Nothing to see here!'

@app.route('/sms', methods=['POST']) # UPDATE FUNCTION
def sms():
	app.logger.info(request.form)
	num = request.form['From']
	inp = request.form['Body']
	if num == NUMBER1 or num == NUMBER2:
		# REMOVE option
		if inp.split()[0] == 'rm':
			sheet = sheetHelper.updateSheet()
			if sheetHelper.delFromSheet( int(inp.split()[1]) ):
				sheet = sheetHelper.updateSheet()
				sendSheet(sheet)
			else:
				client.messages.create(
			        to = num,
			        from_ = NUMBER3,
			        body = "Index is out of bounds"
					)
		# PRINT option
		elif inp.split()[0] == 'print':
			sheet = sheetHelper.updateSheet()
			sendSheet(sheet)
		# ADD option
		else:
			# Update sheet and add
			sheet = sheetHelper.updateSheet()
			sheetHelper.addToSheet(inp)
			sheet = sheetHelper.updateSheet()
			# Send sheet through SMS
			sendSheet(sheet)
			
	return 'hi'

def sendSheet(sheet):
	newSheet = []
	newSheet.append(''.join(sheet['values'][0]))
	del sheet['values'][0]
	count = 1
	for s in sheet['values']:
		newSheet.append(str(count)+'. '+''.join(s))
		count+=1
	
	app.logger.info(count)
	print(newSheet)
	client.messages.create(
        to = num,
        from_ = NUMBER3,
        body = '\n'.join(newSheet)
		)

if __name__ == "__main__":
	app.run(debug = True)
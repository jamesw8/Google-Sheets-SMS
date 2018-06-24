from flask import Flask, request, render_template
from twilio.rest import Client
import requests
import sheetHelper
import os
app = Flask(__name__)

try:
	# f = open('twilioapi', 'r')
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
except:
	# ACCOUNT_SID = os.environ.get("twilio_sid")
	# AUTH_TOKEN = os.environ.get("twilio_token")
	NUMBER1 = os.environ.get("number1")
	NUMBER2 = os.environ.get("number2")
	NUMBER3 = os.environ.get("number3")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/sms', methods=['POST']) # UPDATE FUNCTION
def sms():
	app.logger.info(request.form)
	num = request.form['From']
	inp = request.form['Body']
	if num == NUMBER1 or num == NUMBER2:
		# REMOVE option
		if inp.split()[0].lower() == 'rm':
			sheet = sheetHelper.updateSheet()
			if sheetHelper.delFromSheet( int(inp.split()[1]) ):
				sheet = sheetHelper.updateSheet()
				retval = sendSheet(sheet, num)
			else:
				app.logger.info("Index is out of bounds!")
				'''client.messages.create(
			        to = num,
			        from_ = NUMBER3,
			        body = "Index is out of bounds"
					)'''
		# PRINT option
		elif inp.split()[0].lower() == 'print':
			print('hi')
			sheet = sheetHelper.updateSheet()
			retval = sendSheet(sheet, num)
		# ADD option
		else:
			# Update sheet and add
			sheet = sheetHelper.updateSheet()
			sheetHelper.addToSheet(inp)
			sheet = sheetHelper.updateSheet()
			# Send sheet through SMS
			retval = sendSheet(sheet, num)
	print(retval, type(retval))
	return '<br>'.join(retval)

def sendSheet(sheet, num):
	newSheet = []
	newSheet.append(''.join(sheet['values'][0]))
	del sheet['values'][0]
	count = 1
	for s in sheet['values']:
		newSheet.append(str(count)+'. '+''.join(s))
		count+=1
	
	app.logger.info(count)
	app.logger.info(newSheet)
	'''client.messages.create(
        to = num,
        from_ = NUMBER3,
        body = '\n'.join(newSheet)
		)'''
	return newSheet
if __name__ == "__main__":
	port = os.environ.get("PORT", 5000)
	app.run(host='0.0.0.0', port=port, debug=True)
import os
import flask
import threading
import myCrypto

app = flask.Flask("")


@app.route("/")
def home():
	return flask.render_template("verify.html")


@app.route("/verify", methods=["POST"])
def verify():
	content = flask.request.form["content"]
	signature = flask.request.form["signature"]

	if(content == "" or content is None):
		return "Content is empty"
		
	elif(signature == "" or signature is None):
		return "Signature is empty"

	if(myCrypto.verify(content.strip(), signature.strip(), os.environ["public"])):
		return "Vaild!"
		
	return "Invaild :("


def run():
	app.run(host = '0.0.0.0', port = 8080)


threading.Thread(target = run).start()


while(True):
	input()
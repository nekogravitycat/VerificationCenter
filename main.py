import os
import flask
import threading
import myCrypto
import hashlib

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


@app.route("/sign")
def sign():
	#Verify authority
	token = flask.request.cookies.get("token")
	if(token != os.environ["token"]):
		return flask.render_template("login.html")
		
	return flask.render_template("sign.html")


@app.route("/signature", methods=["POST"])
def signature():
	#Verify authority
	token = flask.request.cookies.get("token")
	if(token != os.environ["token"]):
		return flask.render_template("login.html")
		
	content = flask.request.form["content"]
	signature = myCrypto.sign(content, os.environ["private"])
	return flask.render_template("signature.html", title="signature", content=content, signature=signature)



@app.route("/login", methods = ["POST", "GET"])
def login():
	#For GET method
	if(flask.request.method == "GET"):
		token: str = flask.request.cookies.get("token")
		
		if(token != os.environ["token"]):
			return flask.render_template("login.html")
			
		return flask.redirect("/sign")

	#For POST method
	token = flask.request.form["token"]
	
	if(token != "" or not token is None):
		resp = flask.make_response(flask.redirect("/sign"))
		sha: str = hashlib.sha256(token.encode()).hexdigest()
		resp.set_cookie("token", sha)
		return resp

	return flask.redirect("/login?try-again=1")


@app.route("/public-key")
def show_public_key():
	return os.environ["public"].replace("\n", "<br>")


def run():
	app.run(host = '0.0.0.0', port = 8080)


threading.Thread(target = run).start()


while(True):
	input()
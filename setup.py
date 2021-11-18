from flask import Flask, render_template, request, redirect, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'


import gspread
from oauth2client.service_account import ServiceAccountCredentials

credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
                                                              ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"])

client=gspread.authorize(credential)

gsheet=client.open("pagina").sheet1

@app.route('/')          

def hello_world():

    return  render_template ("inicio2.html") 

@app.route('/registro')          

def registro():

    return  render_template ("registro.html") 

@app.route('/registro2')          

def registro2():

    return  render_template ("registro2.html") 

@app.route('/confirm', methods=["POST"])          

def confirm():
    users= gsheet.get_all_records()
    for user in users:
        if user['email'] == request.form['email'] and user['password'] == request.form['password']:
            session['name'] = user['name']
            session['active'] = True
            return redirect('/nombre')
    flash('Error en Email o Clave')
    return redirect("/registro2")

@app.route('/iniciado')  
def iniciado():

    name=request.form["name"]
    return render_template("iniciado.html",name=name)
@app.route('/excel')  
def excel():

    return jsonify(gsheet.get_all_records())


@app.route('/nombre', methods=["post"])
def nombre():
    name=request.form["name"]
    return render_template("iniciado.html",name=name)


@app.route('/quienes')          

def quienes():

    return  render_template ("quienessomos.html")








if __name__=="__main__":   

    app.run(debug=True)   

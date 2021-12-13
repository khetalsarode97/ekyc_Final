import mysql
from PIL import Image
from flask import Flask, jsonify, request
import text8
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/user_register', methods = ['GET', 'POST'])
def user_register():
	if(request.method == 'POST'):
		myconn = mysql.connector.connect(host="localhost", user="root", database="kyc_api_data")
		cur = myconn.cursor()
		username = request.form.get("username","");
		password = request.form.get("password","");
		if(username!="" and password!=""):
			sql_select_Query = "SELECT * FROM otp WHERE mail LIKE " + "'" + str(username) + "%" + "'"
			cur.execute(sql_select_Query)
			myresult = cur.fetchone()
			if (len(myresult) != 0):
				if (username == myresult[1] and password == myresult[3]):
					return jsonify({"Message":"User is already Registered"})
			else:
				sql = "INSERT INTO otp (mail,password) VALUES (%s, %s)"
				val = (username, password)
				cur.execute(sql, val)
				myconn.commit()
				return jsonify({"Message":"User is Registered Successfully"})
		else:
			return jsonify({"Message":"Username and Password field is empty"})

@app.route('/user_forget_cred', methods = ['GET', 'POST'])
def user_forget_cred():
	if(request.method == 'GET'):
		myconn = mysql.connector.connect(host="localhost", user="root", database="kyc_api_data")
		cur = myconn.cursor()
		username = request.form.get("username","");
		sql_select_Query = "SELECT * FROM otp WHERE mail LIKE " + "'" + str(username) + "%" + "'"
		cur.execute(sql_select_Query)
		myresult = cur.fetchone()
		if(len(myresult)==0):
			return jsonify({"Message":"User not Registered"})
		else:
			return jsonify({"Message":"Your Credientials Here"},{"Credientials":{"Username":username,"Password":myresult[3]}})


@app.route('/extract_data', methods = ['GET', 'POST'])
def home():
	if(request.method == 'POST'):
		myconn = mysql.connector.connect(host="localhost", user="root", database="kyc_api_data")
		cur = myconn.cursor()
		name = fname = number = dob = idtype = state = address = city = zipcode = phnnumber= ""
		username = request.form.get("username","");
		password = request.form.get("password","")
		if(username != "" and password != ""):
			sql_select_Query = "SELECT * FROM otp WHERE mail LIKE " + "'" + str(username) + "%" + "'"
			cur.execute(sql_select_Query)
			myresult = cur.fetchone()
			if(len(myresult)!=0):
				if(username == myresult[1] and password == myresult[3]):
					imagefile = request.files.get('imagefile','')
					if(imagefile.filename.__contains__(".jpeg") or imagefile.filename.__contains__(".jpg") or imagefile.filename.__contains__(".png")):
						imagefile.save("static/1.jpeg")
						try:
							img = Image.open("static/1.jpeg")
							rotate_img = img.rotate(0, expand=True)
							rotate_img.save("static/1.jpeg", quality=100)
						except:
							pass
						name, fname, number, dob, idtype, state, address, city, zipcode, phnnumber, sex, image_path = text8.vali()
						print(name, fname, number, dob, sex,idtype, state, address, city, zipcode, phnnumber, image_path)
						cur.execute("SELECT * FROM identity_details WHERE docnumber LIKE " + "'" + "%" + str(number) + "%" + "'")
						records = cur.fetchall()
						if(len(records)==0):
							sql = "insert into identity_details(name,fname,gender,dob,doctype,docnumber,address,zipcode,city,state,phnumber, mail, document) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
							val = (name, fname, sex, dob, idtype, number, address, zipcode, city, state, phnnumber, username, image_path)
							cur.execute(sql, val)
							myconn.commit()
							full_data = {
									"Message":"Record inserted successfully",
									"Data":{
									"Name": name,
									"Father Name": fname,
									"Document Number": number,
									"Date of Birth": dob,
									"Gender": sex,
									"IDType": idtype,
									"Address": address,
									"City": city,
									"State": state,
									"Zipcode": zipcode,
									"Phone Number": phnnumber,
									"Mail": username}
								}
							return full_data
						else:
							return jsonify({"Message":"Record Already Exist"})
					else:
						return jsonify({"Message": "File Extension Should be in(jpg,jpeg or png)"})
				else:
					return jsonify({"Message":"User does not exist"})
			else:
				return jsonify({"Message": "User does not exist"})
		else:
			return jsonify({"Message":"Crediential not passed"})

@app.route('/get_data', methods = ['GET'])
def get_data():
	if(request.method == 'GET'):
		myconn = mysql.connector.connect(host="localhost", user="root", database="kyc_api_data")
		cur = myconn.cursor()
		docnumber = request.form.get('docnumber',"")
		cur.execute("SELECT * FROM identity_details WHERE docnumber LIKE " + "'" + "%" + str(docnumber) + "%" + "'")
		user_record = cur.fetchone()
		user_data = {
				"Name":user_record[1],
				"FName":user_record[2],
				"Gender":user_record[3],
				"Date_of_Birth":user_record[4],
				"Document_Type":user_record[5],
				"Document_Number":user_record[6],
				"Address":user_record[7],
				"City":user_record[8],
				"State":user_record[9],
				"Zipcode":user_record[10],
				"Phone_Number":user_record[11],
				"Mail_ID":user_record[12]
		}
		if(len(user_record)==0):
			return jsonify({"Message":"Record Does not exist"})
		else:
			return user_data

@app.route('/get_all_data', methods = ['GET'])
def get_all_data():
	if(request.method == 'GET'):
		myconn = mysql.connector.connect(host="localhost", user="root", database="kyc_api_data")
		cur = myconn.cursor()
		ad_username = request.form.get("admin_usr","");
		ad_password = request.form.get("admin_pass","")
		if(ad_username == "admin" and ad_password == "admin123"):
			query = "select * from identity_details"
			cur.execute(query)
			row_headers = [x[0] for x in cur.description]
			user_records = cur.fetchall()
			all_users_data=[]
			for result in user_records:
				all_users_data.append(dict(zip(row_headers, result)))
			return jsonify(all_users_data)
		else:
			return jsonify({"Message":"Admin Credentials not Matched"})

if __name__ == '__main__':
	app.run(debug = True)


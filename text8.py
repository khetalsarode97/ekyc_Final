import random
import re

import cv2
import cv2 as cv
import mysql.connector
import pgeocode
import pytesseract


def vali():
	def adhaar_read_data(text):
		text1 = []
		text0 = []
		data = {}
		text3 = []
		text4 = []
		adhar = name = fname = dob = state = fname = city = zipcode = phnnumber = ""
		idtype = "Aadhar"
		lines = text.split('\n')
		for lin in lines:
			s = lin.strip()
			s = lin.replace('\n', '')
			s = s.rstrip()
			s = s.lstrip()
			text1.append(s)
		text1 = list(filter(None, text1))
		if 'female' in text.lower():
			sex = "FEMALE"
		else:
			sex = "MALE"
		text0 = ["Enrollment No", "Enroliment No", "Government of India", "Aeme ReaH e",
				 "Unique Identification Authority of India", "Enrolment No.:", "--", "Governmentofindia"]
		for i in text1:
			for j in text0:
				if (i.__contains__(j)):
					text1.remove(i)
				else:
					pass
		try:
			adh = []
			for i in text1:
				if (len(i) == 14 and re.match(r'\d{4} \d{4} \d{4}', i)):
					adh.append(i)

			adhar = int(adh[-1].replace(" ", ""))
		except:
			pass
		try:
			if "To" in text1 or "To." in text1:
				for i in text1:
					if (i.startswith("C/O") or i.startswith("S/O") or i.startswith("S0") or i.startswith("W/O")):
						inx = text1.index(i)
						name = text1[inx - 1]
						break
			else:
				for i in text1:
					if (i.__contains__(">") or i.__contains__("-")):
						pass
					else:
						i = re.sub(r'[^\w]', ' ', i)
						i = i.strip()
						if (i[0].isupper() and i[1].islower() and i[2].islower()):
							name = i
							name = ' '.join([w for w in name.split() if len(w) > 1])

							break
		except:
			pass
		# fathers name
		text2 = []
		fname1 = ""
		lines1 = text_all.split('\n')
		for lin in lines1:
			s = lin.strip()
			s = lin.replace('\n', '')
			s = s.rstrip()
			s = s.lstrip()
			text3.append(s)
		text3 = list(filter(None, text3))
		try:
			for i in text3:
				i = re.sub("[^A-Za-z0-9/: ,]", "", i.strip())
				i = i.strip()
				text2.append(i)
			for i in text2:
				if i.startswith('C/O') or i.startswith('C/0') or i.startswith('S/O:') or i.startswith(
						'S/0') or i.startswith("5/0:") or i.startswith("5/0") or i.startswith(
					"510 ") or i.startswith("W/O") or "S/O" in i or " 5/0 " in i or i.startswith(
					"5/0:") or 'Father :' in i or i.__contains__('8/0') or i.__contains__('S0'):

					x = name.split()
					for j in range(len(x)):
						if x[j] in i:
							fname1 = i
							break
					f = fname1.split()
					print(f, "amazon")
					for word in range(len(f)):
						if ',' not in f[word]:
							fname = fname + f[word] + " "
						elif ',' in f[word]:
							fname = fname + f[word] + " "
							break
						else:
							break

					fname = fname.replace("C/O", "")
					fname = fname.replace("/", "")
					fname = fname.replace(":", "")
					fname = fname.replace("at post", "")
					fname = fname.replace("WO", "")
					fname = fname.replace("Address:", "")
					fname = fname.replace("post", "")
					fname = fname.replace("Father", "")
					fname = re.sub('[^A-Za-z/: ]', "", fname.strip())
					fname = fname.replace("SO", "")
					fname = ' '.join([w for w in fname.split() if len(w) > 1])
					break
			print(fname, "father name")
		except:
			pass
		try:
			dt = []
			for i in text1:
				if (i.__contains__("DOB") or i.__contains__("Year of Birth") or i.__contains__("YoB")
						or i.__contains__("Sl B:") or i.__contains__("008") or i.__contains__("जन्म")):
					i = i.replace("DOB", "")
					i = i.replace(":", "")
					dt.append(i)
			# print(dt)
			dt = dt[0].split(" ")
			print(dt, "zimbra")

			# print(dt)
			for i in dt:
				if re.match(r'\d{2}-\d{2}-\d{4}', i) or re.match(r'\d{2}/\d{2}/\d{4}', i):
					dob = i
				elif re.match(r'\d{4}', i):
					dob = i
			if (dob == None):
				dob = dt[-1].replace("DOB:", "").replace("a9YoB:", "")
		except:
			pass
		try:
			zipcode = ""
			for i in text1:
				if (re.findall(r'\d{6}', i)):
					# print(i)
					zipcode = i
					break
			if (zipcode != ""):
				zipcode = re.sub("[^0-9]", "", zipcode)
				zipcode = zipcode[-6:]
				data = pgeocode.Nominatim('IN')
				# print(data.query_postal_code(zipcode))
				state = data.query_postal_code(zipcode).state_name
				city = data.query_postal_code(zipcode).county_name
			else:
				city = state = zipcode = ""
		except:
			pass

		try:
			for i in text1:
				if (len(i) == 10 and i.isnumeric()):
					phnnumber = i
					break
				elif (i.__contains__("Mobile")):
					phnnumber = i[-10:]
					break
			print(phnnumber)
		except:
			pass
		print(name, fname, adhar, dob, idtype, state, zipcode, city, phnnumber)
		return name, fname, adhar, dob, idtype, state, zipcode, city, phnnumber, sex

	def pan_read_data(text):
		name = fname = dob = pan = ""
		idtype = "Pan"
		nameline = []
		dobline = []
		panline = []
		text0 = []
		text1 = []
		text2 = []
		lines = text.split('\n')
		text1 = []
		for lin in lines:
			s = lin.strip()
			s = lin.replace('\n', '')
			s = s.rstrip()
			s = s.lstrip()
			text1.append(s)
		text1 = list(filter(None, text1))
		lineno = 0
		for wordline in text1:
			xx = wordline.split('\n')
			if ([w for w in xx if re.search(
					'(INCOMETAXDEPARTMENT|INCOMETAXDEPARTMENT ~ #!%  GOVT.OFINDIA °|INCOMETAXDEPARTMENT        GOVT OFINDIA|INCOME TAX DEPARTMENT|INCOMETAXDEPARWENT|INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$',
					w)]):
				text1 = list(text1)
				lineno = text1.index(wordline)
				break
		text0 = text1[lineno + 1:]
		text2 = ["TN", "INCOMETAXDEPARTMENT", " ' INCOME TAX DEPAKTMENT", "INCOMETAXDEPARTMENT",
				 "INCOMETAXDEPARTMENT        GOVT OFINDIA",
				 "INCOME TAX DEPARTMENT   GOVT  OF INDLA", "SBMAHY  T T", "INCOME", "INCOME TAX DEPARTMENT",
				 "INCOMETAX DEPARTMENT", "INCOMETAXDEPARWENT", "INCOME", "TAX", "GOW", "GOVT", "GOVERNMENT",
				 "OVERNMENT", "VERNMENT", "DEPARTMENT", "EPARTMENT", "PARTMENT", "ARTMENT", "INDIA", "NDIA"]
		for i in text0:
			if (i in text2):
				text0.remove(i)
		text1 = []
		count = 0
		try:
			for i in text0:
				print(i)

				i = re.sub('[^A-Z0-9_]', ' ', i)
				i = i.strip()
				if (i.isupper() and len(i) > 5):
					text1.append(i)
			# First name
			name = text1[0].strip()
			name = re.sub('[^A-Z] +', ' ', name)
			name = ' '.join([w for w in name.split() if len(w) > 1])
			# Fathers Name
			fname = text1[1].strip()
			fname = ' '.join([w for w in fname.split() if len(w) > 1])
			# Cleaning DOB
			for i in text0:
				if (i.__contains__("-")):
					i = re.sub('[^0-9\/-]', ' ', i)
					i = i.replace("-", "")
					if (re.search(r'\d{2}-\d{2}-\d{4}', i) or re.search(r'\d{2}/\d{2}/\d{4}', i)):
						dob = i.strip()
				elif (re.search(r'\d{2}-\d{2}-\d{4}', i) or re.search(r'\d{2}/\d{2}/\d{4}', i)):
					i = re.sub('[^0-9\/-]', ' ', i)
					dob = i.strip()

			# Cleaning PAN Card details
			print(text0)
			for i in text0:
				i = i.replace(" °", "")
				i = re.sub('[^A-Z0-9_]', ' ', i)
				print(i)
				i = i.strip()
				if ((re.match('^[A-Z0-9]+$', i) and len(i) == 10 and i[-1].isalpha()) or (
						re.match('^[A-Z0-9]+$', i) and len(i) == 11 and i[-1].isalpha())):
					pan = i

		except:
			pass
		return name, fname, dob, pan, idtype

	list_of_states = ['JK-', 'HP-', 'PN-', 'CH-', 'UK-', 'UA-', 'HR-', 'DL-', 'RJ-', 'UP-', 'BR-', 'SK-', 'AR-', 'AS-',
					  'NL-', 'MN-', 'ML-', 'TR-', 'MZ-', 'WB-', 'JH-', 'OR-', 'OD-', 'CG-', 'MP-', 'GJ-', 'MH-', 'DD-',
					  'DN-', 'TS-', 'AP-', 'KA-', 'KL-', 'TN-', 'PY-', 'GA-', 'AN-', 'LD-',
					  'JK', 'HP', 'PN', 'CH', 'UK', 'UA', 'HR', 'DL', 'RJ', 'UP', 'BR', 'SK', 'AR', 'AS', 'NL', 'MN',
					  'ML', 'TR', 'MZ', 'WB', 'JH', 'OR', 'OD', 'CG', 'MP', 'GJ', 'MH', 'DD', 'DN', 'TS', 'AP', 'KA',
					  'KL', 'TN', 'PY', 'GA', 'AN', 'LD']
	data = {}
	types_of_lic = ['MC 50cc', 'LMV-NT', 'FVG', 'MC EX50CC', 'MCWG', 'HGMV', 'HPMV', 'LMV-INVCRG-NT', 'LMV-TR', 'LMV',
					'LDRXCV', 'HMV', 'HTV', 'TRANS', 'INVCRG']

	state_with_name = {'JK-': 'Jammu and Kashmir', 'HP-': 'Himachal Pradesh', 'CH-': 'Chandigarh', 'UK-': 'Uttarakhand',
					   'HR-': 'Haryana', 'DL-': 'Delhi', 'RJ-': 'Rajasthan', 'UP-': 'Uttar Pradesh', 'BR-': 'Bihar',
					   'SK-': 'Gangtok',
					   'AR-': 'Arunachal Pradesh', 'AS-': 'Assam', 'NL-': 'Nagaland', 'MN-': 'Manipur',
					   'ML-': 'Manipur', 'TR-': 'Tripura',
					   'MZ-': 'Mizoram', 'WB-': 'West Bengal', 'JH-': 'JharKhand', 'OR-': 'Orissa',
					   'CG-': 'Chhattisgarh', 'MP-': 'Madhya Pradesh',
					   'GJ-': 'Gujrat', 'MH-': 'Maharashtra', 'DD-': 'Daman and Diu', 'DN-': 'Dadra and Nagar Haveli',
					   'TS-': 'Telangana',
					   'AP-': 'Andra Pradesh', 'KA-': 'Karnataka', 'KL-': 'Kerla', 'TN-': 'TamilNadu',
					   'PY-': 'Pondicherry', 'GA-': 'Goa',
					   'AN-': 'Andaman and Nicobar', 'LD-': 'Lakshadweep', 'PB-': 'Punjab',
					   'JK': 'Jammu and Kashmir', 'HP': 'Himachal Pradesh', 'CH': 'Chandigarh', 'UK': 'Uttarakhand',
					   'HR': 'Haryana', 'DL': 'Delhi', 'RJ': 'Rajasthan', 'UP': 'Uttar Pradesh', 'BR': 'Bihar',
					   'SK': 'Gangtok',
					   'AR': 'Arunachal Pradesh', 'AS': 'Assam', 'NL': 'Nagaland', 'MN': 'Manipur', 'ML': 'Manipur',
					   'TR': 'Tripura',
					   'MZ': 'Mizoram', 'WB-': 'West Bengal', 'JH-': 'JharKhand', 'OR-': 'Orissa',
					   'CG-': 'Chhattisgarh', 'MP-': 'Madhya Pradesh',
					   'GJ': 'Gujrat', 'MH': 'Maharashtra', 'DD': 'Daman and Diu', 'DN': 'Dadra and Nagar Haveli',
					   'TS': 'Telangana',
					   'AP': 'Andra Pradesh', 'KA': 'Karnataka', 'KL': 'Kerla', 'TN': 'TamilNadu', 'PY': 'Pondicherry',
					   'GA': 'Goa',
					   'AN': 'Andaman and Nicobar', 'LD': 'Lakshadweep', 'PB': 'Punjab'}

	def licence_read_data(text):
		licno = name = dob = fname = number = state = city = zipcode = ""
		idtype = "Licence"
		licname = ""
		dobline = []
		text0 = []
		text1 = []
		text2 = []
		data = {}
		lines = text.split('\n')
		for lin in lines:
			s = lin.strip()
			s = lin.replace('\n', '')
			s = s.rstrip()
			s = s.lstrip()
			text1.append(s)
		text1 = list(filter(None, text1))
		print(text1)
		lineno = 0
		try:
			for i in text1:
				if (i.startswith('Licence No. :') or i.startswith('DL No') or i.startswith('No.') or i.startswith(
						'Licence') or i.__contains__('DL No')
						or i.startswith("Dt No") or i.__contains__('DL No')):
					i = i.replace("‘", "")
					licno = i.split(" ")

			print(licno)
			for i in licno:
				# i = re.sub('[:]', '', i)
				for j in list_of_states:
					# i = i.replace("‘", "")
					if (i.startswith(j) and len(i) == 16):
						data['Licence No:'] = i
						number = i

					elif (i.startswith(j) and len(i) == 4):
						inx = licno.index(i) + 1
						number = i + " " + licno[inx]

					elif (i.__contains__(j) and len(i) == 5):
						inx = licno.index(i) + 1
						number = i + " " + licno[inx]
		except:
			pass
		try:
			for i in text1:
				if (i.startswith('Name') or i.startswith('ame') or i.startswith(':') or i.startswith(
						'Vame') or i.startswith('| Name')):
					# i = re.sub('[:]', '', i)
					name = i.split(" ")

					# data['Name']=' '.join(name[1:])
					name = ' '.join(name[1:])
					name = re.sub('[^A-Z]', ' ', name)
					name = ' '.join([w for w in name.split() if len(w) > 1])
					break
				else:
					name = ""
		except:
			pass
		try:

			# fname
			noise = ["5/D/W of", "S/D/W of", "S/DM of", "S/DW of", "S/DIW of", "S/DMW of", "W of"]
			for i in text1:
				for j in noise:
					if (i.__contains__(j)):
						i = i.replace(j, '')
						i = re.sub('[^A-Z]', ' ', i)
						fname = i
						fname = ' '.join([w for w in fname.split() if len(w) > 1])
						break
		except:
			pass

		try:

			for i in text1:
				if (i.startswith('DOB') or i.__contains__('DOl')):
					dob = i.split(" ")
			for j in dob:
				if (len(j) == 10 or len(j) == 8):
					data['Date of Birth'] = j
					dob = j
			if (re.match(r'\d{2}/\d{2}/\d{4}', dob)):
				pass
			elif (re.match(r'\d{2}-\d{2}-\d{4}', dob)):
				dob = dob.replace("-", "/")
			else:
				dob = dob[0:2] + "/" + dob[2:4] + "/" + dob[4:]

		except:
			pass
		try:
			for i in text1:
				if (i.__contains__("PIN") or i.__contains__("Pin") or i.__contains__("pin") or
						i.__contains__("Pia") or i.__contains__("PIV") or i.__contains__("Signature")
						or len(i) == 6):
					if (re.findall(r'\d{6}', i)):
						zipcode = i
						break
				elif (((re.findall(r'\d{6}', i) and len(i) == 8)) or ((re.findall(r'\d{6}', i) and len(i) == 7))
					  or ((re.findall(r'\d{6}', i) and len(i) == 9))):
					zipcode = i
					break
			zipcode = re.sub("[^0-9]", "", zipcode)
			zipcode = zipcode[0:6]
			import pgeocode
			if (zipcode != ""):
				data = pgeocode.Nominatim('IN')
				state = data.query_postal_code(zipcode).state_name
				city = data.query_postal_code(zipcode).community_name
				def isNaN(city):
					return city != city
				if (isNaN(city) == True):
					city = data.query_postal_code(zipcode).county_name
		except:
			pass

		return name, number, dob, state, idtype, fname, city, zipcode
	def passport_read_data(text):
		text1 = []
		text0 = []
		text2 = []
		data = {}
		sym = []
		name = passno = dob = address = ""
		idtype = "Passport"
		text0 = text.split()
		print(text0)
		try:
			for i in text0:
				if (i == 'F'):
					sex = "FEMALE"
				elif (i == 'M'):
					sex = "MALE"
			# print(sex)
			print(text0)
			for i in text0:
				if (len(i) > 2 and i[0].isalpha() and i[1].isnumeric()):
					if (len(i) == 8):
						passno = i
						break
				else:
					j = text0[len(text0) - 1]
					passno = j[0:7]
					passno = passno.replace("®", "0")
					passno = passno.replace("§", "8")

			# print(passno)

			dt = []
			for i in text0:
				if re.search(r'\d{2}-\d{2}-\d{4}', i) or re.search(r'\d{2}/\d{2}/\d{4}', i):
					dt.append(i)
			dob = dt[0]
		except:
			pass
		try:

			text0 = []
			text1 = []
			text0 = text.split("\n")
			print(text0)
			for i in text0:
				if (i.__contains__("/") or i.__contains__(passno) or i.__contains__("_") or i.__contains__(
						"<") or i.__contains__(")")
						or i.__contains__("INDIA") or i.endswith("IND") or i.__contains__(")") or i.__contains__(
							",") or i.__contains__("|")
						or i.__contains__(".") or i.__contains__(":") or i.__contains__(";")):
					pass
				elif (len(i) > 2):
					text1.append(i)
			print(text1)
			text0 = []
			for i in text1:
				if i.strip():
					i = re.sub(r'[\Wa-z0-9 ]', ' ', i)
					print(i, "dabra")
					text0.append(i.strip())
			# text0.append(" ")

			print(text0, "abra")
			while ("" in text0):
				text0.remove("")
			for i in text0:
				c = 0
				for j in range(0, len(i)):
					if i[j] == " ":
						c += 1
				if (c > 2):
					text0.remove(i)
			print(text0)
			name = text0[1].strip() + " " + text0[0]

			text0 = []
			text1 = []
			text0 = text.split("\n")
			print(text0)
			while ("" in text0):
				text0.remove("")
			for i in text0:
				if (i.__contains__("Address")):
					index = text0.index(i)
					for j in range(index + 1, len(text0)):
						if (text0[j].__contains__("PIN")):
							address += text0[j]
							break
						else:
							address += text0[j]
				elif (i.__contains__("ROAD")):
					index = text0.index(i)
					for j in range(index, len(text0)):
						if (text0[j].__contains__("PIN")):
							address += text0[j]
							break
						else:
							address += text0[j]
			print(address)

		except:
			pass

		return passno, name, dob, idtype, address

	def voterid_data_read(text):
		text1 = []
		text0 = []
		text2 = []
		data = {}
		name = votno = fname = dob = ""
		idtype = "Voterid"
		text0 = text.split(" ")
		for lin in text0:
			s = lin.strip()
			s = lin.replace('\n', '')
			s = s.rstrip()
			s = s.lstrip()
			text1.append(s)
		text1 = list(filter(None, text1))
		# print(text1)
		try:
			if 'female' in text.lower():
				sex = "FEMALE"
			else:
				sex = "MALE"
			print(text1, "split")
			for i in text1:
				if ((re.match('^[A-Z0-9]+$', i) and len(i) == 10 and i[-1].isnumeric()) or (
						re.match('^[A-Z0-9]+$', i) and len(i) == 11 and i[-1].isnumeric())):
					votno = i
			if (votno == ""):
				text0 = []
				text2 = pytesseract.image_to_string(image, lang='eng')
				text0 = text2.split("\n")
				print(text0, "split")
				for i in text0:
					if ((re.match('^[A-Z0-9]+$', i) and len(i) == 10 and i[-1].isnumeric()) or (
							re.match('^[‘A-Z0-9]+$', i) and len(i) == 11 and i[-1].isnumeric())):
						votno = i

			text0.clear()
			text1.clear()
			# text2.clear()
			text1 = text.split("\n")
			pattern = ["ELECTOR'S NAME", "Lloctor's Name", "Elector's Name", "ELECTOR’S NAME", "Bectors Name",
					   "Bector’s Name", "Electors Name", "Llectar's Name"]
			for i in text1:
				for j in pattern:
					if (i.__contains__(j)):
						i = i.replace(j, "")
						text0 = i
			text0 = text0.replace("-+", "").replace(":", "")
			name = text0
			name = ' '.join([w for w in name.split() if len(w) > 1])
			print(name)
			# fname
			text0 = []
			text1.clear()
			text1 = text.split("\n")

			pattern = ["Father's Name", "FATHER’S NAME", "FATHER'S NAME", "Father's Name"]
			for i in text1:
				for j in pattern:
					if (i.__contains__(j)):
						i = i.replace(j, "")
						text0 = i
			text0 = text0.replace("-+", "").replace(":", "")
			fname = re.sub('A-Za-z', '', text0)
			fname = ' '.join([w for w in fname.split() if len(w) > 1])
			print(fname)
			for i in text1:
				if (re.search(r'\d{2}/\d{2}/\d{4}', i) or re.search(r'\d{2}-\d{2}-\d{4}', i)):
					dob = i[-10:]
					break
				else:
					dob = ""
			print(dob)
		except:
			pass

		return name, votno, idtype, fname, dob

	def adhar_read_text(res):
		add = ""
		text1 = []
		lines = text.split('\n')
		for lin in lines:
			s = lin.strip()
			s = lin.replace('\n', '')
			s = s.rstrip()
			s = s.lstrip()
			text1.append(s)
		text1 = list(filter(None, text1))

		print(text1)
		text2 = []
		for i in text1:
			i = re.sub("[^A-Za-z0-9/: ]", "", i.strip())
			i = i.strip()
			text2.append(i)
		print(text2)

		while ("" in text2):
			text2.remove("")

		print(text2)
		add = ""

		try:
			for i in text2:
				if (i.__contains__("Address") or i.__contains__("Adaress:") or i.__contains__("400658")):
					for j in range(text2.index(i), len(text2), 1):
						if (len(text2[j]) == 6 and text2[j].isnumeric()):
							add += " "
							add += text2[j]
							break
						elif (len(text2[j]) == 14 or len(text2[j]) == 13 and text2[j][0].isnumeric() or text2[
							j].__contains__("VID")):
							break
						else:
							add += " "
							add += text2[j]
					break
				elif (i.startswith("5/0:") or i.startswith("S0") or i.startswith("C/O") or i.startswith(
						"W/O") or i.startswith("S/O")):
					for j in range(text2.index(i), len(text2), 1):
						if (len(text2[j]) == 10 and text2[j].isnumeric() or text2[j].__contains__("Mobile")):
							break
						else:
							add += " "
							add += text2[j]
					break
			add = add.replace("Address:", "").replace("Adaress:", "").replace("400658", "").replace(":", "")
			print(add)

			def unique_list(l):
				ulist = []
				[ulist.append(x) for x in l if x not in ulist]
				return ulist

			add = ' '.join(unique_list(add.split()))
			print(add)
		except:
			pass

		return add

	def address_licence(text):
		add = ""
		text1 = []
		lines = text.split('\n')
		for lin in lines:
			s = lin.strip()
			s = lin.replace('\n', '')
			s = s.rstrip()
			s = s.lstrip()
			text1.append(s)
		text1 = list(filter(None, text1))

		print(text1)
		text2 = []

		add = ""
		try:
			for i in text1:
				if (i.__contains__("Address") or i.__contains__("Add") or i.__contains__("address") or i.__contains__(
						"add") or i.__contains__("Haaress") or i.__contains__("Acd") or i.__contains__("dd")):
					for j in range(text1.index(i), len(text1), 1):
						if (text1[j].__contains__("PIN") or text1[j].__contains__("Pin") or text1[j].__contains__(
								"pin") or
								text1[
									j].__contains__("Pia") or text1[j].__contains__("PIV") or text1[j].__contains__(
									"Signature")
								or len(text1[j]) == 6):
							# add+=res[j]
							break
						else:
							add += " "
							add += text1[j]
			add = re.sub("[^A-Za-z0-9,-/ ]", "", add)
		except:
			pass
		return add

	def pan_sign_crop():
		image = cv.imread("static/1.jpeg", cv.IMREAD_GRAYSCALE)
		binary = cv.adaptiveThreshold(image, 150, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 15)
		se = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
		se = cv.morphologyEx(se, cv.MORPH_CLOSE, (10, 10))
		mask = cv.dilate(binary, se)

		mask1 = cv.bitwise_not(mask)
		binary = cv.bitwise_and(image, mask)
		result = cv.add(binary, mask1)
		cv2.imwrite("static/result.jpg", result)
		image = cv2.imread("static/result.jpg")
		dimensions = image.shape

		img = cv2.resize(image, (450, 289))
		print(img.shape)
		height, width = img.shape[0], img.shape[1]

		crop_img = img[215:height - 15, 0:230]
		cv2.imwrite("static/sign.jpg", crop_img)
		im = cv2.imread("static/sign.jpg")

		height, width = im.shape[0], im.shape[1]
		crop_img_new = im[5:height - 4, 2:width - 10]
		cv2.imwrite("static/sign.jpg", crop_img_new)

	try:
		# global image
		image = cv2.imread("static/1.jpeg")
		img = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		text = pytesseract.image_to_string(img, lang='eng')
		text_all = pytesseract.image_to_string(img, lang='eng+mar+hin')
		print(text)
		name = number = dob = idtype = state = address = data = city = zipcode = phnnumber = ""
		myconn = mysql.connector.connect(host="localhost", user="root", database="form_data")
		cur = myconn.cursor()
		global image_id
		image_id = random.randint(100, 500)
		# print(text)
		if "election" in text.lower() or "commission" in text.lower():
			name = fname = number = dob = idtype = state = address = city = zipcode = phnnumber = sex = image_path = ""
			name, number, idtype, fname, dob = voterid_data_read(text)
			print(name, number, idtype, fname, dob)
			data = text
			cv2.imwrite("static//documents//" + str(number) + ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
			image_path = "/static/documents/" + str(number) + ".jpg"
			sql = "insert into identity_details(name,docnumber,doctype,fname,dob,document) values(%s,%s,%s,%s,%s,%s)"
			val = (name, number, idtype, fname, dob, image_path)
			#cur.execute(sql, val)
			#myconn.commit()
			return name,fname, number, dob, idtype, state, address, city, zipcode, phnnumber, sex, image_path
		elif "income" in text.lower() or "tax" in text.lower():
			name = fname = number = dob = idtype = state = address = image_path = city = zipcode = phnnumber = sex = ""
			# name,number,dob,idtype = pan_read_data(text)
			name, fname, dob, number, idtype = pan_read_data(text)
			data = " ".join(text)
			if (number == ""):
				image = cv.imread("static/1.jpeg", cv.IMREAD_GRAYSCALE)
				binary = cv.adaptiveThreshold(image, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 15)
				se = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
				se = cv.morphologyEx(se, cv.MORPH_CLOSE, (2, 2))
				mask = cv.dilate(binary, se)

				mask1 = cv.bitwise_not(mask)
				binary = cv.bitwise_and(image, mask)
				result = cv.add(binary, mask1)
				# cv2.imshow(result)
				cv2.imwrite("static/result.jpg", result)
				image = cv2.imread("static/result.jpg")
				img = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
				img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				text = pytesseract.image_to_string(img, lang='eng')
				print(text)
				data = text
				name, fname, dob, number, idtype = pan_read_data(text)
				print(number,"pannumber")
			cv2.imwrite("static//documents//" + str(number) + ".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
			image_path = "/static/documents/" + str(number) + ".jpg"
			sql = "insert into identity_details(name,docnumber,dob,doctype,fname,document) values(%s,%s,%s,%s,%s,%s)"
			val = (name, number, dob, idtype, fname, image_path)
			pan_sign_crop()
			#cur.execute(sql, val)
			#myconn.commit()
			return name,fname, number, dob, idtype, state, address, city, zipcode, phnnumber, sex, image_path
		elif "licence" in text.lower() or "drive" in text.lower():
			name = fname = number = dob = idtype = state = address = image_path = city = zipcode = phnnumber = sex = ""
			name, number, dob, state, idtype, fname, city, zipcode = licence_read_data(text)
			data = " ".join(text)
			if address == "":
				text = ""
				image = cv2.imread("static/1.jpeg")
				img = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
				img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				text = pytesseract.image_to_string(img, lang='eng')

				address = address_licence(text)
				data = " ".join(text)
			cv2.imwrite("static//documents//" + str(number) + ".jpg", image,
						[int(cv2.IMWRITE_JPEG_QUALITY), 100])
			image_path = "/static/documents/" + str(number) + ".jpg"
			#sql = "insert into identity_details(name,docnumber,dob,state,doctype,fname,address,city,zipcode,document) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			#val = (name, number, dob, state, idtype, fname, address, city, zipcode, image_path)
			return name, fname, number, dob, idtype, state, address, city, zipcode, phnnumber, sex, image_path
		elif "indian" in text.lower() or "republic" in text.lower():
			name = fname = number = dob = idtype = state = address = city = zipcode = phnnumber = sex = image_path = ""
			number, name, dob, idtype, address = passport_read_data(text)
			print(number, name, dob, idtype, address)
			data = text
			cv2.imwrite("static//documents//" + str(number) + ".jpg", image,
						[int(cv2.IMWRITE_JPEG_QUALITY), 100])
			image_path = "/static/documents/" + str(number) + ".jpg"
			sql = "insert into identity_details(name,docnumber,dob,doctype,document,address) values(%s,%s,%s,%s,%s,%s)"
			val = (name, number, dob, idtype, image_path, address)
			#cur.execute(sql, val)
			#myconn.commit()
			return name, fname, number, dob, idtype, state, address, city, zipcode, phnnumber, sex, image_path
		elif "male" in text.lower():
			name = fname = number = dob = idtype = state = address = image_path = city = zipcode = phnnumber = sex = ""
			name, fname, number, dob, idtype, state, zipcode, city, phnnumber, sex = adhaar_read_data(text)
			data = " ".join(text)
			if address == "":
				text = ""
				image = cv2.imread("static/1.jpeg")
				img = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
				img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				text = pytesseract.image_to_string(img, lang='eng+hin+mar+tam')
				address = adhar_read_text(text)
				data = " ".join(text)
			cv2.imwrite("static//documents//" + str(number) + ".jpg", image,
						[int(cv2.IMWRITE_JPEG_QUALITY), 100])
			image_path = "/static/documents/" + str(number) + ".jpg"
			sql = "insert into identity_details(name,fname,docnumber,dob,doctype,state,address,zipcode,city,phnumber,document,gender) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			val = (name, fname, number, dob, idtype, state, address, zipcode, city, phnnumber, image_path, sex)
			#cur.execute(sql, val)
			#myconn.commit()
			return name,fname, number, dob, idtype, state, address, city, zipcode, phnnumber, sex, image_path
	except:
		print("Data Not extracted")
		myconn.rollback()
	myconn.close()
	#return cur.lastrowid, data

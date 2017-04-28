#Copyright {yyyy} {name of copyright owner}

  # Licensed under the Apache License, Version 2.0 (the "License");
   #you may not use this file except in compliance with the License.
   #You may obtain a copy of the License at

    #   http://www.apache.org/licenses/LICENSE-2.0

   #Unless required by applicable law or agreed to in writing, software
   #distributed under the License is distributed on an "AS IS" BASIS,
   #WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   #See the License for the specific language governing permissions and
   #limitations under the License.
   # Author: Roberto Ruiz

import http.client
import json
import http.server

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	OPENFDA_API_URL="api.fda.gov"
	OPENFDA_API_EVENT="/drug/event.json"
	OPEN_DRUG="/drug/event.json?search=patient.drug.medicinalproduct:"
	OPEN_COMPANY="/drug/event.json?search=companynumb:"
	def get_main_page(self):
		html = """
		<html>
			<head>
				<title>Open FDA Cool App</title>
			</head>
			<body>
				<h1>OpenFDA Client</h1>
				<form method="get" action="listDrugs">
					<input type="submit" value="Drugs List">
					</input>
					Limit:
					<input type= "text" name="limit">
					</input>
				</form>

				<form method="get" action="searchDrug">
					Drug name:
					<input type="submit" value="Search Companies"> </input>
					<input type="text" name="Drug"> </input>
				</form>
				<form method="get" action="listCompanies">
					<input type="submit" value="Companies list">
					</input>
					Limit:
					<input type="text" name="limit">
					</input>
				</form>
				<form method="get" action="searchCompany">
					Company name:
					<input type="submit" value="Search Drugs"> </input>
					<input type="text" name="Company"> </input>
				</form>
				<form method="get" action="listGender">
					<input type= "submit" value="Genders List">
					</input>
					Limit:
					<input type="text" name="limit">
					</input>
				</form>
			</body>
		</html>
		"""
		return html

	def get_event_html(self,lista):

		html_event="""
		<html>
			<head></head>
			<body>
		  		<ol>
		"""
		for i in lista:
			html_event+="<li>"+i+"</l1>"
		html_event+="""
				</ol>
			</body>
		</html>
		"""
		return html_event

	def get_event(self):

		limit=self.word_sep()
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request("GET",self.OPENFDA_API_EVENT +"?limit="+limit)
		r1 = conn.getresponse()
		print (r1.status,r1.reason)
		data = r1.read()
		data1=data.decode("utf8")
		return data1

	def get_company(self):

		DRUG=self.word_sep()
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request("GET",self.OPEN_COMPANY+DRUG+"&limit=10")
		r1 = conn.getresponse()
		print (r1.status,r1.reason)
		data= r1.read()
		data1=data.decode("utf8")
		return data1

	def get_drug(self):

		DRUG=self.word_sep()
		conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
		conn.request("GET",self.OPEN_DRUG+DRUG+"&limit=10")
		r1 = conn.getresponse()
		print (r1.status,r1.reason)
		data = r1.read()
		data1=data.decode("utf8")
		return data1

	def word_sep(self):
		drug1=self.path.split('=')[1]
		return drug1

	def get_company_drug_by_drug(self):

		events=self.get_drug()
		events=json.loads(events)
		company=[]
		for event in events["results"]:
			company=company+[event["companynumb"]]
		return company

	def get_drug_company_by_company(self):

		events=self.get_company()
		events=json.loads(events)
		company=[]
		for event in events ["results"]:
			company=company+[event["patient"]["drug"][0]["medicinalproduct"]]
		return company

	def do_GET(self):

		main_page=False
		is_event=False
		is_search_drug=False
		is_search_company=False
		is_event_company=False
		is_event_gender=False
		is_error=False
		is_found=False

		if self.path=='/':
			main_page=True
			is_found=True
		elif "listDrugs" in self.path:
			is_event=True
			is_found=True
		elif "searchDrug" in self.path:
			is_search_drug=True
			is_found=True
		elif "searchCompany" in self.path:
			is_search_company=True
			is_found=True
		elif "listCompanies" in self.path:
			is_event_company=True
			is_found=True
		elif "listGender" in self.path:
			is_event_gender=True
			is_found=True
		else:
			is_error=True
		if is_found:
			self.send_response(200)
		else:
			self.send_response(404)


		self.send_header('Content-type','text/html')
		self.end_headers()
		html= self.get_main_page()

		if main_page:

			self.wfile.write(bytes(html, "utf8"))

		elif is_event:

			event=self.get_event()
			event=json.loads(event)
			lista=[]
			event1=event["results"]
			for event in event1:
				event2=event["patient"]["drug"][0]["medicinalproduct"]
				event3=json.dumps(event2)
				lista+=[event3]
			self.wfile.write(bytes(self.get_event_html(lista), "utf8"))

		elif is_search_drug:
			search=self.get_company_drug_by_drug()
			html_drug=self.get_html_company(search)
			self.wfile.write(bytes(html_drug,"utf8"))

		elif is_search_company:

			search=self.get_drug_company_by_company()
			html_1=self.get_html_drug(search)
			self.wfile.write(bytes(html_1,"utf8"))

		elif is_event_company:
			event=self.get_event()
			event=json.loads(event)
			event1=event["results"]
			lista=[]
			for event in event1:
				event2=event["companynumb"]
				event3=json.dumps(event2)
				lista+=[event3]
			self.wfile.write(bytes(self.get_html_company(lista),"utf8"))

		elif is_event_gender:

			event=self.get_event()
			event=json.loads(event)
			lista=[]
			event1=event["results"]
			for event in event1:
				event2=event["patient"]["patientsex"]
				event3=json.dumps(event2)
				lista+=[event3]
			self.wfile.write(bytes(self.get_html_gender(lista), "utf8"))

		elif is_error:

			self.wfile.write(bytes(self.get_html_error(), "utf8"))

	def get_event_html(self,lista):

		html_event="""
		<html>
			<head></head>
			<body>
				<h1> DRUGS </h1>
		  		<ol>
		"""
		for i in lista:
			html_event+="<li>"+i+"</l1>"
		html_event+=""" </ol>
			</body>
		</html>
		"""
		return html_event

	def get_html_drug(self,lista):

		html_event="""
		<html>
			<head></head>
			<body>
				<h1> DRUGS </h1>
				<ol>
		"""
		for i in lista:
			html_event+="<li>"+i+"</li>"
		html_event+="""
				</ol>
			</body>
		</html>
		"""
		return html_event

	def get_html_company(self,lista):
		html_event="""
		<html>
			<head></head>
			<body>
				<h1> COMPANIES </h1>
				<ol>
		"""
		for i in lista:
			html_event+="<li>"+i+"</li>"
		html_event+="""
				</ol>
			</body>
		</html>
		"""
		return html_event

	def get_html_gender(self,lista):

		html_event="""
		<html>
			<head></head>
			<body>
				<h1> GENDERS </h1>
				<ol>
		"""
		for i in lista:
			html_event+="<li>"+i+"</li>"
		html_event+="""
				</ol>
			</body>
		</html>
		"""
		return html_event

	def get_html_error(self):

		html_event_error="""
		<html>
			<head></head>
			<body>
				<h1> ERROR 404 <h1>
			</body>
		</html>
		"""
		return html_event_error

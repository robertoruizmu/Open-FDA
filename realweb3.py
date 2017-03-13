import http.client
import json
import http.server

#ESTE ES EL QUE FUNCIONA


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	# GET
	OPENFDA_API_URL="api.fda.gov"
	OPENFDA_API_EVENT="/drug/event.json"

	def get_main_page(self):
		html = """
		<html>
			<head>
				<title>Open FDA Cool App</title>
			</head>
			<body>
				<h1>OpenFDA Client</h1>
				<form method="get" action="receive">
					<input type="submit" value="Enviar a OpenFDA">
					</input>
				</form>
				<form method="get" action="search">
					<input type="submit" value="Drug search LYRICA: Enviar a OpenFDA">
					</input>
					<input type="text" name="drug"></input>
				</form>
			</body>
		</html>
		"""
		return html
# aqui cambiamos lo de limit 1 por limit 10 para que nos coja 10 eventos
	def get_event_html(self,lista):
		#en la funcion metemos lo que hay en el archivo algo.py
		html_event="""
		<html>
			<head></head>
			<body>
		  		<ul>
		"""
		for i in lista:
			html_event+="<li>"+i+"</l1>"
		html_event+="""
				</ul>
			</body>
		</html>
		"""
		return html_event
	OPEN_LYRICA="/drug/event.json?search=patient.drug.medicinalproduct:"
	def get_event(self):
			conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
			conn.request("GET",self.OPENFDA_API_EVENT + "?limit=10")
			r1 = conn.getresponse() #guarda la respuesta
			print (r1.status,r1.reason)
			data1 = r1.read() # devuelve el contenido
			data1=data1.decode("utf8") #pasa de bytes a stream

			return data1
	def get_any_drug(self):
		drug1=self.path.split["="][1]
		return drug1
	def get_lyrica(self):
			DRUG=self.get_any_drug()
			conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
			conn.request("GET",self.OPEN_LYRICA + DRUG + "&limit=10")
			r1 = conn.getresponse() #guarda la respuesta
			print (r1.status,r1.reason)
			data1 = r1.read() # devuelve el contenido
			data1=data1.decode("utf8") #pasa de bytes a stream

			return data1
			#self.path es la ruta de la url
	def get_lyrica_company(self):
		events=self.get_lyrica()
		company=[]
		for event in events['results']:
			company=company+[event["companynumb"]]
		return company
	def do_GET(self):
		main_page=False
		is_event=False
		is_search=False
		if self.path=='/':
			main_page=True
		elif self.path=='/receive?':
			is_event=True
		elif self.path=='/search?Drug=':
			is_search=True
		# Send response status code
		self.send_response(200)
		# Send headers
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send message back to client
		#message = "Hello world! " + self.path
		# Write content as utf-8 data

		html= self.get_main_page()
		if main_page:
			self.wfile.write(bytes(html, "utf8"))
		elif is_event:
			event=self.get_event()
			event=json.loads(event)
			lista=[]
			for i in range(10):
				results=event["results"][i]["patient"]["drug"][0]["medicinalproduct"]
				lista=lista+[results] #el result tiene que ir dentro de una lista
			#array=",".join(lista) # esto se hace para separar las cosas de la lista con comas
			#print (array)
			self.wfile.write(bytes(self.get_event_html(lista), "utf8")) #aqui ponia event pero ponemos array pq la info esta ahora ahi
			#lo meto dentro de la condicion para que se ejecute solo al dar al boton
		elif is_search:
			search1=self.get_lyrica_company
			html1=self.html_lyrica(search1)
			self.wfile.write(bytes(html1,"utf-8"))
		return
#AHORA YA NO SALEN EN EL LOCALHOST LOS 10 MEDICAMENTOS QUE SE HAN COGIDO DEL json
#HAY QUE CONSEGUIR QUE SALGA EN VERTICAL EN LUGAR DE HORIZONTAL
	def get_event_html(self,lista):
		#en la funcion metemos lo que hay en el archivo algo.py
		html_event="""
		<html>
			<head></head>
			<body>
		  		<ul>
		"""
		for i in lista:
			html_event+="<li>"+i+"</l1>"
		html_event+="""
				</ul>
			</body>
		</html>
		"""
		return html_event
	def html_lyrica(self,lista):
		html_event="""
		<html>
			<head></head>
			<body>
				<h1> MEDICAMENTOS </h1>
				<ul>
		"""
		for i in lista:
			hmtl_event+="<li>"+i+"</li>"
		html_event+="""
				</ul>
			</body>
		</html>
		"""
		return html_event

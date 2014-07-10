# -*- encoding: utf-8 -*-
import reportlab

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


class Invoice2PDF:
	def __init__(self, type, file):
		self.file = file
		self.type = type
		self.p = canvas.Canvas(self.file, pagesize=A4, bottomup=0)
		self.width, self.height = A4
		self.left = 0
		self.p.scale(0.982, 0.982)
		self.p.translate(2*mm, 2*mm)
		self.index = 0
		self.sum = 0
		self.sumvat = 0
		
	def drawLines(self):
		#horizontal lines
		self.p.setLineWidth(.3*mm)
		self.drawFullLine(65)
		self.drawFullLine(170)
			
	def drawProductHeader(self, invoice):
		if invoice.info1 == "":
			self.start = 70
		else:
			self.start = 85
			self.p.drawString(20*mm, (self.start-15)*mm, invoice.info1)
		self.p.setFont("Helvetica-Bold", 10)
		self.p.drawString(10*mm, self.start*mm, "#")
		self.p.drawString(20*mm, self.start*mm, "Nimi")
		self.p.drawString(80*mm, self.start*mm, "Määrä")
		self.p.drawString(100*mm, self.start*mm, "á-hinta")
		self.p.drawString(120*mm, self.start*mm, "Ale-%")
		self.p.drawString(135*mm, self.start*mm, "Alv-%")
		self.p.drawString(150*mm, self.start*mm, "Veroton")
		self.p.drawString(180*mm, self.start*mm, "Verollinen")
			
	def drawProduct(self, name, count, each, vat, discount):
		self.index +=1
		offset = 7
		self.p.setFont("Helvetica", 10)
		self.p.drawString(10*mm, (self.start+self.index*offset)*mm, str(self.index))
		self.p.drawString(20*mm, (self.start+self.index*offset)*mm, name)
		self.p.drawString(80*mm, (self.start+self.index*offset)*mm, str(count))
		self.p.drawString(100*mm, (self.start+self.index*offset)*mm, str(each))
		self.p.drawString(120*mm, (self.start+self.index*offset)*mm, str(discount))
		self.p.drawString(135*mm, (self.start+self.index*offset)*mm, str(vat))
		self.sum += count*each-(count*each*(float(discount)/100))
		self.p.drawString(150*mm, (self.start+self.index*offset)*mm, str(count*each-(count*each*(float(discount)/100))))
		self.sumvat += count*each*(1+(float(vat)/100))-count*each*(1+(float(vat)/100))*(float(discount)/100)
		self.p.drawString(180*mm, (self.start+self.index*offset)*mm, str(count*each*(1+(float(vat)/100))-count*each*(1+(float(vat)/100))*(float(discount)/100)))
		
	def drawProductFooter(self, invoice):
		self.index += 1
		offset = 7
		self.p.setLineWidth(.2*mm)
		self.drawFullLine((self.start+self.index*offset)-4)
		self.p.setFont("Helvetica-Bold", 10)
		self.p.drawString(20*mm, (self.start+self.index*offset)*mm, "Veroton")
		self.p.drawString(50*mm, (self.start+self.index*offset)*mm, "Vero")
		self.p.drawString(80*mm, (self.start+self.index*offset)*mm, "Verollinen")
	
		self.p.drawString(130*mm, (self.start+self.index*offset)*mm, "Yhteensä")
		self.p.drawString(150*mm, (self.start+self.index*offset)*mm, str(self.sum))
		self.p.drawString(180*mm, (self.start+self.index*offset)*mm, str(self.sumvat))
		self.index += 1
		offset = 7
		self.p.setFont("Helvetica", 10)
		self.p.drawString(20*mm, (self.start+self.index*offset-3)*mm, str(self.sum))
		self.p.drawString(50*mm, (self.start+self.index*offset-3)*mm, str(self.sumvat-self.sum))
		self.p.drawString(80*mm, (self.start+self.index*offset-3)*mm, str(self.sumvat))
		self.index += 1
		if invoice.info2 != "":
			self.p.drawString(20*mm, (self.start+self.index*offset-5)*mm, invoice.info2)
			
	def drawInvoiceInfo(self, invoice):
		if self.type == "invoice":
			types = "Lasku"
		if self.type == "receipt":
			types = "Kuitti"
		if self.type == "reminder":
			types = "Maksuhuomautus"
		# draws all the fields
		#self.p.setDash(False)
		self.p.setStrokeColorRGB(0,0,0)
		self.p.rect(110*mm, 10*mm, 85*mm, 5*mm)
		self.p.setFont("Helvetica-Bold", 12)
		self.p.drawString(112*mm, 13.5*mm, types)
		'''
		self.date = date
		self.id = invoice_id
		self.ref = ref
		self.client_id = client_id
		self.our_ref = our_ref
		self.your_ref = your_ref
		self.payment_type = payment_type
		self.due_date = due_date
		self.reclamation_time = reclamation_time
		self.penalty_interest = penalty_interest
		self.sum = sum
		'''
		fields = ("Päivämäärä", "Laskun numero", "Asiakasnumero", "Eräpäivä", "Huomautusaika", "Viivästyskorko-%", "Viitteenne", "Viitteemme")
		values = (invoice.date, invoice.id, invoice.client_id, invoice.due_date, invoice.reclamation_time, invoice.penalty_interest, invoice.your_ref, invoice.our_ref)
		self.p.setFont("Helvetica", 11)
		i=0
		for field in fields:
			self.p.drawString(110*mm, (20+i)*mm, field)
			i += 5
		i=0
		for value in values:
			self.p.drawString(150*mm, (20+i)*mm, value)
			i += 5
	
	def populateWindow(self, company, payer):
		self.drawWindowValue(company.name+"\n"+company.address+"\n"+company.zipcode+" "+company.city, (20, 13), False)
		self.drawWindowValue(payer.name+"\n"+payer.address+"\n"+payer.zipcode+" "+payer.city, (20, 40))
	
	def drawFooter(self, company):
		#height 180
		self.p.setFont("Helvetica-Bold", 10)
		self.p.drawString(10*mm, 180*mm, company.name)
		self.p.setFont("Helvetica", 10)
		self.p.drawString(10*mm, 185*mm, company.address)
		self.p.drawString(10*mm, 189*mm, company.zipcode+" "+company.city)
		
		#second col
		if company.website != "":
			self.p.drawString(80*mm, 180*mm, company.website)
		self.p.drawString(80*mm, 185*mm, "Puh. "+company.phone)
		self.p.drawString(80*mm, 189*mm, company.email)
		
		#third col
		self.p.drawString(145*mm, 185*mm, "Kotipaikka "+company.homeplace)
		self.p.drawString(145*mm, 189*mm, "Y-tunnus "+company.companyid)		
	
	def populateBankform(self, company, invoice, payer):
		self.drawBankformValue(company.iban, (120, 199))
		self.drawBankformValue(company.bic, (170, 199))
		self.drawBankformValue(company.name, (21, 216))
		
		self.drawBankformValue("Laskun numero\n"+invoice.id, (120, 216))
		self.drawBankformValue(invoice.ref, (124,257))
		if self.type == "reminder":
			self.drawBankformValue("HETI", (124,265))	
		else:
			self.drawBankformValue(invoice.due_date, (124,265))
		self.drawBankformValue(invoice.sum, (170,265))
		
		self.drawBankformValue(payer.name+"\n"+payer.address+"\n"+payer.zipcode+" "+payer.city, (22, 230))
	def drawCutline(self):
		#cutline
		self.p.setDash([2, 2], 0)
		self.drawFullLine(195)
		
	def drawBankform(self):
		#horizontal fulllines
		self.drawFullLine(211)
		self.drawFullLine(260)
		self.drawFullLine(268)
		#horizontal partlines
		self.drawPartLine(226, 110)
		self.drawPartLine(252, 100, 110)
		#vertical lines
		#saajan tiedot
		self.drawVLine(195, 31, 20)
		#middle
		self.drawVLine(195, 73, 110)
		#viite, era
		self.drawVLine(252, 16, 123)
		#bic
		self.drawVLine(195, 16, 160)
		# euro
		self.drawVLine(260, 8, 160)
		#tililta
		self.p.setLineWidth(.13*mm)
		self.drawVLine(260, 8, 20)
		#allek
		self.p.line(21*mm, 255*mm, 110*mm, 255*mm)
		#texts
		self.drawBankformLabel("Saajan\ntilinumero\nMottagarens\nkontonummer", (19,199))
		self.drawBankformLabel("IBAN", (118,199))
		self.drawBankformLabel("BIC", (168,199))
		self.drawBankformLabel("Saaja\nMottagare", (19,216))
		self.drawBankformLabel("Maksaja\nBetalare", (19,230))
		self.drawBankformLabel("Allekirjoitus\nUnderskrift", (19,254))
		self.drawBankformLabel(u"Tililtä nro\nFrån konto nr", (19,263))
		
		self.drawBankformLabel("Viitenro\nRef.nr", (121,255))
		self.drawBankformLabel(u"Eräpäivä\nFörf.dag", (121,263))
		self.drawBankformLabel(u"Euro", (168,263))
		
	def drawFullLine(self, height):
		self.p.line(0+self.left, height*mm, self.width, height*mm)
		
	def drawBankformLabel(self, text, pos):
		self.p.setFont("Helvetica", 7)
		x, y = pos
		lines = text.split("\n")
		i=0
		for line in lines:
			self.p.drawRightString(x*mm, (y+i)*mm, line)
			i += 2.5

	def drawWindowValue(self, text, pos, big=True):
		if big:
			self.p.setFont("Helvetica", 15)
			s=6
		else:
			self.p.setFont("Helvetica", 11)
			s=4
		x, y = pos
		lines = text.split("\n")
		i=0
		for line in lines:
			self.p.drawString(x*mm, (y+i)*mm, line)
			i += s

	def drawBankformValue(self, text, pos):
		self.p.setFont("Helvetica", 10)
		x, y = pos
		lines = text.split("\n")
		i=0
		for line in lines:
			self.p.drawString(x*mm, (y+i)*mm, line)
			i += 4	

	def drawPartLine(self, height, width, padding=0):
		self.p.line((padding+self.left)*mm, height*mm, (padding+width+self.left)*mm, height*mm)
		
	def drawVLine(self, height, lenght, padding):
		self.p.line((padding+self.left)*mm, height*mm, (padding+self.left)*mm, (height+lenght)*mm)
		
	def createInvoice(self, invdata, company, client):
		self.invdata = invdata
		self.drawInvoiceInfo(invdata)
		self.drawProductHeader(invdata)
		self.populateWindow(company, client)
		if self.type != "receipt":
			self.drawBankform()
			self.populateBankform(company, invdata, client)
		self.drawFooter(company)
		
	def ready(self):
		self.drawProductFooter(self.invdata)
		self.drawLines()
		self.drawCutline()
	
	def save(self):
		self.p.showPage()
		self.p.save()


class Company():
	def __init__(self, name, address, zipcode, city, phone, email, homeplace, companyid, iban, bic, website=""):
		self.name = name
		self.address = address
		self.zipcode = zipcode
		self.city = city
		self.phone = phone
		self.email = email
		self.homeplace = homeplace
		self.companyid = companyid
		self.iban = iban
		self.bic = bic
		self.website = website
		
class InvoiceData():
	def __init__(self, date, invoice_id, ref, client_id, our_ref, your_ref, payment_type, due_date, reclamation_time, penalty_interest, sum, info1="", info2=""):
		self.date = date
		self.id = invoice_id
		self.ref = ref
		self.client_id = client_id
		self.our_ref = our_ref
		self.your_ref = your_ref
		self.payment_type = payment_type
		self.due_date = due_date
		self.reclamation_time = reclamation_time
		self.penalty_interest = penalty_interest
		self.sum = sum
		self.info1 = info1
		self.info2 = info2
		
class Client():
	def __init__(self, name, address, zipcode, city):
		self.name = name
		self.address = address
		self.zipcode = zipcode
		self.city = city

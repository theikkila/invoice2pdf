# -*- encoding: utf-8 -*-
import finv2pdf

f2 = finv2pdf
# Company sign: (name, address, zipcode, city, phone, email, homeplace, companyid, iban, bic, website=""):
company = f2.Company("Firma Oy", "Yritystie 2", "00000", "Helsinki", "+358400000000", "support@yritys.fi", "Helsinki", "3333333-3", "FI00 0000 0000 0000 00", "BICFIHH")
# InvoiceData sign: (date, invoice_id, ref, client_id, our_ref, your_ref, payment_type, due_date, reclamation_time, penalty_interest, sum, info1="", info2="")
invdata = f2.InvoiceData("3.8.2012", "43", "437", "8", "", "", "14 pv netto", "17.8.2012", "7 vrk", "8", "22,00", "Info 1", "Info 2")
# Client sign: (name, address, zipcode, city)
client = f2.Client("Asiakas Asikainen", "Asiakkaankuja 32", "99999", "Helsinki")
		
		
response = open("lasku.pdf", "w")
# Types: (invoice|receipt|reminder)
inv = f2.Invoice2PDF("invoice", response)
inv.createInvoice(invdata, company, client)
for i in range(1, 10):
	inv.drawProduct("Tuote", i, 21.5, 23, 0)
inv.ready()
inv.save()

response.close()

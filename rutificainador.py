#!/usr/bin/python3

from bs4 import BeautifulSoup
from texttable import Texttable
from pwn import *
import sys,signal,requests,time,re,csv,pdb,string

def def_handler(sig,frame):
	print("\n[!] Saliendo...\n")
	sys.exit(1)

#ctrl+c
signal.signal(signal.SIGINT, def_handler)

# variables globales
url = "https://www.nombrerutyfirma.com/rut"
headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50'}
header_csv = ['Nombre','RUT','Sexo','Direccion','Ciudad/Comuna']
temp = "0.0.0-0"

def imprimir(datos):
	t = Texttable()
	t.add_rows([['Nombre','RUT','Sexo','Direccion','Ciudad/Comuna'],\
		[datos["nombre"],datos["rut"],datos["sexo"],datos["direccion"],datos["ciucom"]]])
	print(t.draw())

def exportar_datos(datos):
	multiples = True if "-l" in sys.argv else False
	if(multiples):
		data = [datos["nombre"],datos["rut"],datos["sexo"],datos["direccion"],datos["ciucom"]]
		with open('resultados_rut.csv','a',encoding='UTF-8') as r:
			writer = csv.writer(r)
			writer.writerow(data)
	else:
		data = [datos["nombre"],datos["rut"],datos["sexo"],datos["direccion"],datos["ciucom"]]
		with open('resultados_rut.csv','w',encoding='UTF-8') as r:
			writer = csv.writer(r)
			writer.writerow(header_csv)
			writer.writerow(data)


def procesar(res):
	exportar = True if "-e" in sys.argv else False
	td = res.find_all('td')
	if(td):
		datos = {
			"nombre":td[0].get_text(),"rut":td[1].get_text(),"sexo":td[2].get_text(),
			"direccion":td[3].get_text(),"ciucom":td[4].get_text()
		}
		if(exportar):
			exportar_datos(datos)
		else:
			imprimir(datos)
	else:
		print("\x1b[1;31m"+f"El rut {temp} no existe o el digito verificador esta mal\n")

def consulta(payload):
	s = requests.Session()
	res = s.post(url,data=payload,headers=headers)
	time.sleep(2)
	procesar(BeautifulSoup(res.text,'lxml'))

def main():
	p1 = log.progress("Recopilando informacion")
	global temp
	if("-r" in sys.argv):
		i  = sys.argv.index("-r")
		rut = sys.argv[i+1]
		if(re.search("[0-9]{1,2}.[0-9]{3}.[0-9]{3}-[0-9,k,K]",rut)):
			payload = {'term':rut}
			temp = rut.rstrip("\n")
			consulta(payload)
		else:
			print("El formato debe ser 12.123.123-0\nSi termina en k o no lo sabes, reemplazalo por un 0\n")
			sys.exit(1)
	elif("-l" in sys.argv):
		p1.status("Probando RUTs multiples")
		i = sys.argv.index("-l")
		ruts = open(sys.argv[i+1],"r")
		with open('resultados_rut.csv','w',encoding='UTF-8') as r:
			writer = csv.writer(r)
			writer.writerow(header_csv)

		for rut in ruts:
			if(re.search("[0-9]{1,2}.[0-9]{3}.[0-9]{3}-[0-9,k,K]",rut)):
				payload = {'term':rut.rstrip("\n")}
				temp = rut.rstrip("\n")
				consulta(payload)
			else:
				print("El formato debe ser 12.123.123-0\nSi no lo sabes, reemplazalo por un 0\n")
				continue	

if __name__ == '__main__':
	main()
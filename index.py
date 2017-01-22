#!C:\Python36\python.exe
from __future__ import print_function
import sys

from flask import Flask, render_template
import json


def bondis():
	f = open('recorrido_colectivos.csv', 'r')

	f.readline()  # saltea el encabezado

	res = {}
	lineas = []
	terminales = []
	recorridos = []
	count = 0
	for register in f:
		cols = register.split(';')
		linea = get_linea(cols[2])
		add_linea(lineas, linea)

		

		lngLats = cols[0][13:len(cols[0]) - 2].split(',')
		lngLat = lngLats[0].split()
		sentido = cols[5]
		res["sentido"] = sentido

		#if 'IDA' in sentido:
			#add_terminal(terminales, lngLat, linea)

		#if linea == '132':
		recorrido = get_recorrido(cols[0])
		recorridos.append(recorrido)
			#recorrido = cols[0]
			#lngLat = recorrido[13:len(recorrido) - 2].split(',')
			#res['linea39'] = repr(lngLat[0])
		count += 1
	res['recorridos'] = recorridos
	res['terminales'] = terminales
	res['cant_lineas'] = len(lineas)
	res['lineas'] = lineas
	#print(res['lineas'], file=sys.stderr)
	return json.JSONEncoder().encode(res)


# Saca las comillas del numero de linea
def get_linea(col):
	return col[1:len(col) - 1]


def add_linea(lineas, linea):
	if linea not in lineas:
		lineas.append(linea)
	return


def get_recorrido(colRecorrido):
	recorrido = []
	lngLats = colRecorrido[13:len(colRecorrido) - 2].split(',')
	for lngLat in lngLats:
		lngLat = lngLat.split()
		parada = {'lng': float(lngLat[0]), 'lat': float(lngLat[1])}
		#print(parada, file=sys.stderr)

		recorrido.append(parada)

	return recorrido


def add_terminal(terminales, lngLat, linea):
	terminal = {}
	terminal['lat'] = lngLat[1]
	terminal['lng'] = lngLat[0]
	terminal['name'] = "linea_" + linea
	terminales.append(terminal)
	return


app = Flask(__name__)


@app.route("/")
def main():
	a = bondis()
	return render_template('mapa.html', models=a)

if __name__ == "__main__":
	app.run(debug=True)

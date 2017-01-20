#!C:\Python36\python.exe


from flask import Flask, render_template
import json


def bondis():
	f = open('recorrido_colectivos.csv', 'r')

	f.readline()  # saltea el encabezado

	res = {}
	lineas = []
	terminales = []
	count = 0
	for register in f:
		cols = register.split(';')
		linea = cols[2][1:len(cols[2]) - 1]  # las lineas vienen con comillas
		add_linea(lineas, linea)

		recorrido = cols[0]
		lngLats = recorrido[13:len(recorrido) - 2].split(',')
		lngLat = lngLats[0].split()

		sentido = cols[5]
		res["sentido"] = sentido
		if 'IDA' in sentido:
			add_terminal(terminales, lngLat, linea)

		if linea == '39':
			recorrido = cols[0]
			lngLat = recorrido[13:len(recorrido) - 2].split(',')
			res['linea39'] = repr(lngLat[0])

		count += 1
	res['terminales'] = terminales
	res['cant_lineas'] = len(lineas)
	res['lineas'] = lineas
	return json.JSONEncoder().encode(res)


def add_linea(lineas, linea):
	if linea not in lineas:
		lineas.append(linea)
	return


def add_recorrido():
	return


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

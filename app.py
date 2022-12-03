from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from tarea import Tarea
from bson.objectid import ObjectId

db = dbase.dbCnn()

app = Flask(__name__)

@app.route('/')
def index():
    tareas = db['tarea']
    tareasRecibidas = tareas.find()
    return render_template('index.html', tareas=tareasRecibidas)

@app.route('/searchTarea', methods=['POST'])
def searchTarea():
    tareas = db['tarea']
    buscar = request.form['busqueda']
    if buscar:
        tareasRecibidas = tareas.find({'nombre': buscar})
    else:
        tareasRecibidas = tareas.find()
    return render_template('index.html', tareas=tareasRecibidas)

@app.route('/createTarea')
def createTarea():
    return render_template('create.html')

@app.route('/tarea', methods=['POST'])
def storeTarea():
    tareas = db['tarea']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    fechaEntrega = request.form['fechaEntrega']
    materia = request.form['materia']

    if nombre and descripcion and fechaEntrega and materia:
        tarea = Tarea(nombre, descripcion, fechaEntrega, materia)
        tareas.insert_one(tarea.toDBCollection())
        response = jsonify({
            'nombre': nombre,
            'descripcion': descripcion,
            'fechaEntrega': fechaEntrega,
            'materia': materia
        })
        return redirect(url_for('index'))
    else:
        return notFound()

@app.route('/tareaDel/<string:dato>')
def deleteTarea(dato):
    tareas = db['tarea']
    tareas.delete_one({'_id': ObjectId(dato)})
    return redirect(url_for('index'))

@app.route('/tareaEdit/<string:dato>')
def editTarea(dato):
    tareas = db['tarea']
    tareaRecibida = tareas.find({'_id': ObjectId(dato)})
    return render_template('edit.html', row=tareaRecibida)

@app.route('/tareaUpdate/<string:dato>', methods=['POST'])
def updateTarea(dato):
    tareas = db['tarea']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    fechaEntrega = request.form['fechaEntrega']
    materia = request.form['materia']

    if nombre and descripcion and fechaEntrega and materia:
        tareas.update_one({'_id': ObjectId(dato)}, {'$set': {'nombre': nombre, 'descripcion': descripcion, 'fechaEntrega': fechaEntrega, 'materia': materia}})
        response = jsonify({'message': 'La tarea ' + nombre + ' actualizado correctamente'})
        return redirect(url_for('index'))
    else: 
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(debug=True, port=4500)
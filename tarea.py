class Tarea:
    def __init__(self, nombre, descripcion, fechaEntrega, materia):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaEntrega = fechaEntrega
        self.materia = materia
    
    def toDBCollection(self):
        return{
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fechaEntrega': self.fechaEntrega,
            'materia': self.materia
        }
from flask_restx import Namespace, Resource, fields
from app import db
from app.models.user import DomiciliarioModel  # Asegúrate de importar correctamente tu modelo

domiciliario_ns = Namespace('domiciliarios', description='Operaciones CRUD para domiciliarios')

# Modelo para la serialización de datos
domiciliario_model = domiciliario_ns.model('DomiciliarioModel', {
    'id': fields.Integer(readonly=True),
    'nombre': fields.String(required=True, description='Nombre del domiciliario'),
    'apellido': fields.String(required=True, description='Apellido del domiciliario'),
    'cedula': fields.String(required=True, description='Cédula del domiciliario'),
    'telefono': fields.String(required=True, description='Teléfono del domiciliario'),
    'estado': fields.String(required=True, description='Estado del domiciliario'),
    'administrador_id': fields.Integer(required=True, description='ID del administrador relacionado')
})

@domiciliario_ns.route('/')
class DomiciliarioList(Resource):
    @domiciliario_ns.marshal_list_with(domiciliario_model)
    def get(self):
        """Obtener todos los domiciliarios"""
        return DomiciliarioModel.query.all()

    @domiciliario_ns.expect(domiciliario_model)
    def post(self):
        """Crear un nuevo domiciliario"""
        data = domiciliario_ns.payload
        nuevo_domiciliario = DomiciliarioModel(
            nombre=data['nombre'],
            apellido=data['apellido'],
            cedula=data['cedula'],
            telefono=data['telefono'],
            estado=data['estado'],
            administrador_id=data['administrador_id']
        )
        db.session.add(nuevo_domiciliario)
        db.session.commit()
        return {'message': 'Domiciliario creado exitosamente'}, 201

@domiciliario_ns.route('/<int:id>')
class DomiciliarioResource(Resource):
    @domiciliario_ns.marshal_with(domiciliario_model)
    def get(self, id):
        """Obtener un domiciliario por ID"""
        return DomiciliarioModel.query.get_or_404(id)

    @domiciliario_ns.expect(domiciliario_model)
    def put(self, id):
        """Actualizar un domiciliario por ID"""
        domiciliario = DomiciliarioModel.query.get_or_404(id)
        data = domiciliario_ns.payload
        domiciliario.nombre = data['nombre']
        domiciliario.apellido = data['apellido']
        domiciliario.cedula = data['cedula']
        domiciliario.telefono = data['telefono']
        domiciliario.estado = data['estado']
        domiciliario.administrador_id = data['administrador_id']
        db.session.commit()
        return {'message': 'Domiciliario actualizado exitosamente'}, 200

    def delete(self, id):
        """Eliminar un domiciliario por ID"""
        domiciliario = DomiciliarioModel.query.get_or_404(id)
        db.session.delete(domiciliario)
        db.session.commit()
        return {'message': 'Domiciliario eliminado exitosamente'}, 200
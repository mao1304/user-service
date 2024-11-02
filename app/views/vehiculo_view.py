# from flask_restx import Namespace, Resource, fields
# from app import db
# from app.models.user import VehiculoModel  # Asegúrate de importar correctamente tu modelo

# vehiculo_ns = Namespace('vehiculos', description='Operaciones CRUD para vehículos')

# # Modelo para la serialización de datos
# vehiculo_model = vehiculo_ns.model('VehiculoModel', {
#     'id': fields.Integer(readonly=True),
#     'color': fields.String(required=True, description='Color del vehículo'),
#     'marca': fields.String(required=True, description='Marca del vehículo'),
#     'placa': fields.String(required=True, description='Placa del vehículo'),
#     'domiciliario_id': fields.Integer(required=True, description='ID del domiciliario relacionado')
# })

# @vehiculo_ns.route('/')
# class VehiculoList(Resource):
#     @vehiculo_ns.marshal_list_with(vehiculo_model)
#     def get(self):
#         """Obtener todos los vehículos"""
#         return VehiculoModel.query.all()

#     @vehiculo_ns.expect(vehiculo_model)
#     def post(self):
#         """Crear un nuevo vehículo"""
#         data = vehiculo_ns.payload
#         nuevo_vehiculo = VehiculoModel(
#             color=data['color'],
#             marca=data['marca'],
#             placa=data['placa'],
#             domiciliario_id=data['domiciliario_id']
#         )
#         db.session.add(nuevo_vehiculo)
#         db.session.commit()
#         return {'message': 'Vehículo creado exitosamente'}, 201

# @vehiculo_ns.route('/<int:id>')
# class VehiculoResource(Resource):
#     @vehiculo_ns.marshal_with(vehiculo_model)
#     def get(self, id):
#         """Obtener un vehículo por ID"""
#         return VehiculoModel.query.get_or_404(id)

#     @vehiculo_ns.expect(vehiculo_model)
#     def put(self, id):
#         """Actualizar un vehículo por ID"""
#         vehiculo = VehiculoModel.query.get_or_404(id)
#         data = vehiculo_ns.payload
#         vehiculo.color = data['color']
#         vehiculo.marca = data['marca']
#         vehiculo.placa = data['placa']
#         vehiculo.domiciliario_id = data['domiciliario_id']
#         db.session.commit()
#         return {'message': 'Vehículo actualizado exitosamente'}, 200

#     def delete(self, id):
#         """Eliminar un vehículo por ID"""
#         vehiculo = VehiculoModel.query.get_or_404(id)
#         db.session.delete(vehiculo)
#         db.session.commit()
#         return {'message': 'Vehículo eliminado exitosamente'}, 200

from flask_restx import Namespace, Resource, fields
from app import db
from app.models.user import VehiculoModel  # Asegúrate de importar correctamente tu modelo

vehiculo_ns = Namespace('vehiculos', description='Operaciones CRUD para vehículos')

# Modelo para la serialización de datos
vehiculo_model = vehiculo_ns.model('VehiculoModel', {
    'placa': fields.String(required=True, description='Placa del vehículo'),
    'color': fields.String(required=True, description='Color del vehículo'),
    'marca': fields.String(required=True, description='Marca del vehículo'),
    'domiciliario_cedula': fields.String(required=True, description='Cédula del domiciliario relacionado')
})

@vehiculo_ns.route('/')
class VehiculoList(Resource):
    @vehiculo_ns.marshal_list_with(vehiculo_model)
    def get(self):
        """Obtener todos los vehículos"""
        return VehiculoModel.query.all()

    @vehiculo_ns.expect(vehiculo_model)
    def post(self):
        """Crear un nuevo vehículo"""
        data = vehiculo_ns.payload
        nuevo_vehiculo = VehiculoModel(
            placa=data['placa'],
            color=data['color'],
            marca=data['marca'],
            domiciliario_cedula=data['domiciliario_cedula']
        )
        db.session.add(nuevo_vehiculo)
        db.session.commit()
        return {'message': 'Vehículo creado exitosamente'}, 201

@vehiculo_ns.route('/<string:placa>')
class VehiculoResource(Resource):
    @vehiculo_ns.marshal_with(vehiculo_model)
    def get(self, placa):
        """Obtener un vehículo por placa"""
        return VehiculoModel.query.get_or_404(placa)

    @vehiculo_ns.expect(vehiculo_model)
    def put(self, placa):
        """Actualizar un vehículo por placa"""
        vehiculo = VehiculoModel.query.get_or_404(placa)
        data = vehiculo_ns.payload
        vehiculo.color = data['color']
        vehiculo.marca = data['marca']
        vehiculo.domiciliario_cedula = data['domiciliario_cedula']
        db.session.commit()
        return {'message': 'Vehículo actualizado exitosamente'}, 200

    def delete(self, placa):
        """Eliminar un vehículo por placa"""
        vehiculo = VehiculoModel.query.get_or_404(placa)
        db.session.delete(vehiculo)
        db.session.commit()
        return {'message': 'Vehículo eliminado exitosamente'}, 200
# from flask_restx import Namespace, Resource, fields
# from app import db
# from app.models.user import DomiciliarioModel  # Asegúrate de importar correctamente tu modelo

# domiciliario_ns = Namespace('domiciliarios', description='Operaciones CRUD para domiciliarios')

# # Modelo para la serialización de datos
# domiciliario_model = domiciliario_ns.model('DomiciliarioModel', {
#     'id': fields.Integer(readonly=True),
#     'nombre': fields.String(required=True, description='Nombre del domiciliario'),
#     'apellido': fields.String(required=True, description='Apellido del domiciliario'),
#     'cedula': fields.String(required=True, description='Cédula del domiciliario'),
#     'telefono': fields.String(required=True, description='Teléfono del domiciliario'),
#     'estado': fields.String(required=True, description='Estado del domiciliario'),
#     'administrador_id': fields.Integer(required=True, description='ID del administrador relacionado')
# })

# @domiciliario_ns.route('/')
# class DomiciliarioList(Resource):
#     @domiciliario_ns.marshal_list_with(domiciliario_model)
#     def get(self):
#         # """Obtener todos los domiciliarios"""
#         return DomiciliarioModel.query.all()

#     @domiciliario_ns.expect(domiciliario_model)
#     def post(self):
#         """Crear un nuevo domiciliario"""
#         data = domiciliario_ns.payload
#         nuevo_domiciliario = DomiciliarioModel(
#             nombre=data['nombre'],
#             apellido=data['apellido'],
#             cedula=data['cedula'],
#             telefono=data['telefono'],
#             estado=data['estado'],
#             administrador_id=data['administrador_id']
#         )
#         db.session.add(nuevo_domiciliario)
#         db.session.commit()
#         return {'message': 'Domiciliario creado exitosamente'}, 201

# @domiciliario_ns.route('/<int:id>')
# class DomiciliarioResource(Resource):
#     @domiciliario_ns.marshal_with(domiciliario_model)
#     def get(self, id):
#         """Obtener un domiciliario por ID"""
#         return DomiciliarioModel.query.get_or_404(id)

#     @domiciliario_ns.expect(domiciliario_model)
#     def put(self, id):
#         """Actualizar un domiciliario por ID"""
#         domiciliario = DomiciliarioModel.query.get_or_404(id)
#         data = domiciliario_ns.payload
#         domiciliario.nombre = data['nombre']
#         domiciliario.apellido = data['apellido']
#         domiciliario.cedula = data['cedula']
#         domiciliario.telefono = data['telefono']
#         domiciliario.estado = data['estado']
#         domiciliario.administrador_id = data['administrador_id']
#         db.session.commit()
#         return {'message': 'Domiciliario actualizado exitosamente'}, 200

#     def delete(self, id):
#         """Eliminar un domiciliario por ID"""
#         domiciliario = DomiciliarioModel.query.get_or_404(id)
#         db.session.delete(domiciliario)
#         db.session.commit()
#         return {'message': 'Domiciliario eliminado exitosamente'}, 200


from flask_restx import Namespace, Resource, fields
from app import db
from app.models.user import DomiciliarioModel  # Asegúrate de importar correctamente tu modelo


domiciliario_ns = Namespace('domiciliarios', description='Operaciones CRUD para domiciliarios')

# Modelo para la serialización de datos
domiciliario_model = domiciliario_ns.model('DomiciliarioModel', {
    'cedula': fields.String(required=True, description='Cédula del domiciliario'),
    'password':fields.String(required=True, description='contraseña del domiciliario'),
    'nombre': fields.String(required=True, description='Nombre del domiciliario'),
    'apellido': fields.String(required=True, description='Apellido del domiciliario'),
    'telefono': fields.String(required=True, description='Teléfono del domiciliario'),
    'estado': fields.String(required=True, description='Estado del domiciliario'),
    'administrador_usuario': fields.String(required=True, description='Usuario del administrador relacionado')
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
            cedula=data['cedula'],
            password = data['password'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data['telefono'],
            estado=data['estado'],
            administrador_usuario=data['administrador_usuario']
        )
        db.session.add(nuevo_domiciliario)
        db.session.commit()
        return {'message': 'Domiciliario creado exitosamente'}, 201

@domiciliario_ns.route('/<string:cedula>')
class DomiciliarioResource(Resource):
    @domiciliario_ns.marshal_with(domiciliario_model)
    def get(self, cedula):
        """Obtener un domiciliario por cédula"""
        return DomiciliarioModel.query.get_or_404(cedula)

    @domiciliario_ns.expect(domiciliario_model)
    def put(self, cedula):
        """Actualizar un domiciliario por cédula"""
        domiciliario = DomiciliarioModel.query.get_or_404(cedula)
        data = domiciliario_ns.payload
        domiciliario.nombre = data['nombre']
        domiciliario.apellido = data['apellido']
        domiciliario.telefono = data['telefono']
        domiciliario.estado = data['estado']
        domiciliario.administrador_usuario = data['administrador_usuario']
        db.session.commit()
        return {'message': 'Domiciliario actualizado exitosamente'}, 200

    def delete(self, cedula):
        """Eliminar un domiciliario por cédula"""
        domiciliario = DomiciliarioModel.query.get_or_404(cedula)
        db.session.delete(domiciliario)
        db.session.commit()
        return {'message': 'Domiciliario eliminado exitosamente'}, 200
login_dimi_model = domiciliario_ns.model('LoginDomiModel', {
    'usuario': fields.String(required=True, description='Usuario del domiciliario'),
    'password': fields.String(required=True, description='password del domiciliario')
})
@domiciliario_ns.route('/login')
class LoginResource(Resource):
    @domiciliario_ns.expect(login_dimi_model)
    def post(self):
        data = domiciliario_ns.payload
        cedula = data['usuario']
        password = data['password']

        cliente = DomiciliarioModel.query.filter_by(cedula=cedula).first()
        domiID = cliente.cedula
        if cliente and cliente.check_password(password):
            # access_token = create_access_token(identity=usuario)
            return { 'message': 'Login exitoso', 'domiID': domiID}, 200
        else:
            return {'message': 'Credenciales inválidas'}, 401

logout_domi_model = domiciliario_ns.model('LogoutModel', {})

@domiciliario_ns.route('/logout')
class LogoutResource(Resource):
    @domiciliario_ns.expect(logout_domi_model)
    # @jwt_required()
    def post(self):
        return {'message': 'Logout exitoso'}, 200
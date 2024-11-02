from flask_restx import Namespace, Resource, fields
from app import db
from app.models.user import ClienteModel  # Asegúrate de importar correctamente tu modelo

cliente_ns = Namespace('clientes', description='Operaciones CRUD para clientes/ login y logout')


login_model = cliente_ns.model('LoginModel', {
    'usuario': fields.String(required=True, description='Usuario del cliente'),
    'password': fields.String(required=True, description='password del cliente')
})

# Modelo para la serialización de datos
cliente_model = cliente_ns.model('ClienteModel', {
    'usuario': fields.String(required=True, description='Usuario del cliente'),
    'nombre': fields.String(required=True, description='Nombre del cliente'),
    'password': fields.String(required=True, description='password del cliente')
})

@cliente_ns.route('/')
class ClienteList(Resource):
    @cliente_ns.marshal_list_with(cliente_model)
    def get(self):
        """Obtener todos los clientes"""
        return ClienteModel.query.all()

    @cliente_ns.expect(cliente_model)
    def post(self):
        """Crear un nuevo cliente"""
        data = cliente_ns.payload
        nuevo_cliente = ClienteModel(
            usuario=data['usuario'],
            nombre=data['nombre'],
            password=data['password']
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        return {'message': 'Cliente creado exitosamente'}, 201

@cliente_ns.route('/<string:usuario>')
class ClienteResource(Resource):
    @cliente_ns.marshal_with(cliente_model)
    def get(self, usuario):
        """Obtener un cliente por usuario"""
        return ClienteModel.query.get_or_404(usuario)

    @cliente_ns.expect(cliente_model)
    def put(self, usuario):
        """Actualizar un cliente por usuario"""
        cliente = ClienteModel.query.get_or_404(usuario)
        data = cliente_ns.payload
        cliente.nombre = data['nombre']
        cliente.password = data['password']
        db.session.commit()
        return {'message': 'Cliente actualizado exitosamente'}, 200

    def delete(self, usuario):
        """Eliminar un cliente por usuario"""
        cliente = ClienteModel.query.get_or_404(usuario)
        db.session.delete(cliente)
        db.session.commit()
        return {'message': 'Cliente eliminado exitosamente'}, 200


@cliente_ns.route('/login')
class LoginResource(Resource):
    @cliente_ns.expect(login_model)
    def post(self):
        data = cliente_ns.payload
        usuario = data['usuario']
        password = data['password']

        cliente = ClienteModel.query.filter_by(usuario=usuario).first()
        if cliente and cliente.check_password(password):
            # access_token = create_access_token(identity=usuario)
            return { 'message': 'Login exitoso'}, 200
        else:
            return {'message': 'Credenciales inválidas'}, 401

logout_model = cliente_ns.model('LogoutModel', {})

@cliente_ns.route('/logout')
class LogoutResource(Resource):
    @cliente_ns.expect(logout_model)
    # @jwt_required()
    def post(self):
        return {'message': 'Logout exitoso'}, 200
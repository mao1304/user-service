from flask_restx import Namespace, Resource, fields
# from app import db
from app.models.user import AdministradorModel

administrador_ns = Namespace('administradores', description='Operaciones CRUD para administradores')

# Modelo para la serialización de datos
administrador_model = administrador_ns.model('AdministradorModel', {
    'id': fields.Integer(readonly=True),
    'usuario': fields.String(required=True, description='Nombre de usuario'),
    'contraseña': fields.String(required=True, description='Contraseña'),
    'correo': fields.String(required=True, description='Correo electrónico'),
    'compania': fields.String(required=True, description='Compañía')
})

@administrador_ns.route('/')
class AdministradorList(Resource):
    @administrador_ns.marshal_list_with(administrador_model)
    def get(self):
        return AdministradorModel.query.all()

    @administrador_ns.expect(administrador_model)
    def post(self):
        data = administrador_ns.payload
        nuevo_administrador = AdministradorModel(
            usuario=data['usuario'],
            contraseña=data['contraseña'],
            correo=data['correo'],
            compania=data['compania']
        )
        db.session.add(nuevo_administrador)
        db.session.commit()
        return {'message': 'Administrador creado exitosamente'}, 201

@administrador_ns.route('/<int:id>')
class AdministradorResource(Resource):
    @administrador_ns.marshal_with(administrador_model)
    def get(self, id):
        return AdministradorModel.query.get_or_404(id)

    @administrador_ns.expect(administrador_model)
    def put(self, id):
        administrador = AdministradorModel.query.get_or_404(id)
        data = administrador_ns.payload
        administrador.usuario = data['usuario']
        administrador.contraseña = data['contraseña']
        administrador.correo = data['correo']
        administrador.compania = data['compania']
        db.session.commit()
        return {'message': 'Administrador actualizado exitosamente'}, 200

    def delete(self, id):
        administrador = AdministradorModel.query.get_or_404(id)
        db.session.delete(administrador)
        db.session.commit()
        return {'message': 'Administrador eliminado exitosamente'}, 200

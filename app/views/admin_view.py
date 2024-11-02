import json
from flask import jsonify
from flask_restx import Namespace, Resource, fields
from app import db
from app.models.user import AdministradorModel
from app.utils.utils import obtener_repartidor_cercano

administrador_ns = Namespace('administradores', description='Operaciones CRUD para administradores')

# Modelo para la serialización de datos
administrador_model = administrador_ns.model('AdministradorModel', {
    'id': fields.Integer(readonly=True),
    'usuario': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='password'),
    'correo': fields.String(required=True, description='Correo electrónico'),
    'compania': fields.String(required=True, description='Compañía')
})
asignar_pedido = administrador_ns.model('apedido', {
    'id': fields.Integer(readonly=True),
    'pedido_lat': fields.String(required=True, description='Nombre de usuario'),
    'pedido_long': fields.String(required=True, description='password'),

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
            password=data['password'],
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
        administrador.password = data['password']
        administrador.correo = data['correo']
        administrador.compania = data['compania']
        db.session.commit()
        return {'message': 'Administrador actualizado exitosamente'}, 200

    def delete(self, id):
        administrador = AdministradorModel.query.get_or_404(id)
        db.session.delete(administrador)
        db.session.commit()
        return {'message': 'Administrador eliminado exitosamente'}, 200

import redis 
from geopy.distance import geodesic
import json

r = redis.Redis(
  host='redis-10062.c114.us-east-1-4.ec2.redns.redis-cloud.com',
  port=10062,
  password='WihZVLCgfWgerlvLn4p9AUHpnO9yMwYa')
@administrador_ns.route("/asignar_pedido")
class AsignarPedido(Resource):
    @administrador_ns.expect(asignar_pedido) 
    def post(self):
        data = administrador_ns.payload

        pedido_lat = float(data["pedido_lat"])
        pedido_long = float(data["pedido_long"])
        print(f"lat{pedido_lat} long{pedido_long}")
        repartidor_id = obtener_repartidor_cercano(pedido_lat, pedido_long)
        print(f"rep id {repartidor_id}")
        if repartidor_id:
            try:
                # Convertir repartidor_id a string si no lo es
                r.hset("repartidores", str(repartidor_id), json.dumps({"disponible": False}))
                return {"status": "asignado"}, 200
            except Exception as e:
                print(f"Error al actualizar Redis: {e}")
                return {"status": "error", "message": "No se pudo actualizar el estado del repartidor"}, 500
        else:
            return {"status": "sin_repartidor_disponible"}, 404
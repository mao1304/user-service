from flask_restx import Namespace, Resource, fields
from app import db
from app.models.user import PedidoModel  # Asegúrate de importar correctamente tu modelo
import requests
pedido_ns = Namespace('pedidos', description='Operaciones CRUD para pedidos')

# Modelo para la serialización de datos
pedido_model = pedido_ns.model('PedidoModel', {
    'id': fields.Integer(required=True, description='ID del pedido'),
    'direccion_entrega': fields.String(required=True, description='Dirección de entrega del pedido'),
    'direccion_salida': fields.String(required=True, description='Dirección de salida del pedido'),
    'precio': fields.Float(required=False, description='Precio del pedido'),
    'distancia': fields.Float(required=False, description='Distancia del pedido'),
    'cliente_usuario': fields.String(required=True, description='Usuario del cliente relacionado'),
    'domiciliario_cedula': fields.String(required=False, description='Cédula del domiciliario relacionado')
})

@pedido_ns.route('/')
class PedidoList(Resource):
    @pedido_ns.marshal_list_with(pedido_model)
    def get(self):
        """Obtener todos los pedidos"""
        return PedidoModel.query.all()

    @pedido_ns.expect(pedido_model)
    def post(self):
        """Crear un nuevo pedido"""
        data = pedido_ns.payload
        nuevo_pedido = PedidoModel(
            direccion_entrega=data['direccion_entrega'],
            direccion_salida=data['direccion_salida'],
            precio=data['precio'],
            distancia=data['distancia'],
            cliente_usuario=data['cliente_usuario'],
            domiciliario_cedula=data['domiciliario_cedula']
        )
        db.session.add(nuevo_pedido)
        db.session.commit()
        # return {'message': 'calculando precio y distancia'}, 200
        url = "https://graphhopper.com/api/1/route"

        query = {
        "profile": "scooter",
        "point": [data['direccion_salida'], data['direccion_entrega']],
        "locale": "en",
        "instructions": "true",
        "calc_points": "true",
        "debug": "false",
        "points_encoded": "true",
        "key": "eb8e5296-c15d-400b-b969-d7cb6b51bd8b"
        }

        response = requests.get(url, params=query)

        data = response.json()
        distancia_total = data['paths'][0]['distance']
        print(distancia_total)
        return {'message': 'Pedido creado exitosamente', 'data': data}, 201

@pedido_ns.route('/<int:id>')
class PedidoResource(Resource):
    @pedido_ns.marshal_with(pedido_model)
    def get(self, id):
        """Obtener un pedido por ID"""
        return PedidoModel.query.get_or_404(id)

    @pedido_ns.expect(pedido_model)
    def put(self, id):
        """Actualizar un pedido por ID"""
        pedido = PedidoModel.query.get_or_404(id)
        data = pedido_ns.payload
        pedido.direccion_entrega = data['direccion_entrega']
        pedido.direccion_salida = data['direccion_salida']
        pedido.precio = data['precio']
        pedido.distancia = data['distancia']
        pedido.cliente_usuario = data['cliente_usuario']
        pedido.domiciliario_cedula = data['domiciliario_cedula']
        db.session.commit()
        return {'message': 'Pedido actualizado exitosamente'}, 200

    def delete(self, id):
        """Eliminar un pedido por ID"""
        pedido = PedidoModel.query.get_or_404(id)
        db.session.delete(pedido)
        db.session.commit()
        return {'message': 'Pedido eliminado exitosamente'}, 200
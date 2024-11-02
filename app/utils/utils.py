import redis 
from geopy.distance import geodesic
import json

r = redis.Redis(
  host='redis-10062.c114.us-east-1-4.ec2.redns.redis-cloud.com',
  port=10062,
  password='WihZVLCgfWgerlvLn4p9AUHpnO9yMwYa')

def obtener_repartidor_cercano(pedido_lat, pedido_long):
    print("entro a la funcion")
    # Obtener todos los repartidores disponibles de Redis
    repartidores = r.hgetall("repartidores")
    repartidor_mas_cercano = None
    distancia_minima = float("inf")
    
    for repartidor_id, data in repartidores.items():
        print("entro al for")
        data = json.loads(data)
        print(f"domis{data}")
        if data.get("disponible"):
            repartidor_lat = data["latitude"]
            repartidor_long = data["longitude"]
            print(f"lat repartidor: {repartidor_lat} long repartidor: {repartidor_long}")
            print(f"lat pedido: {pedido_lat} long pedido: {pedido_long}")
            distancia = geodesic((pedido_lat, pedido_long), (repartidor_lat, repartidor_long)).km
            print(f"distancia: {distancia}")
            if distancia < distancia_minima:
                distancia_minima = distancia
                repartidor_mas_cercano = repartidor_id

    return repartidor_mas_cercano 
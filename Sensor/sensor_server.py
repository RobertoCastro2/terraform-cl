import time
import random
from concurrent import futures

import grpc
import sensor_pb2
import sensor_pb2_grpc

class SensorServicer(sensor_pb2_grpc.SensorServicer):
    def StreamReadings(self, request, context):
        sensor_id = request.sensor_id
        while True:
            # Simula leitura de temperatura entre 20°C e 30°C
            value = random.uniform(20.0, 30.0)
            timestamp = int(time.time() * 1000)
            reading = sensor_pb2.Temperature(
                sensor_id=sensor_id,
                value=value,
                timestamp=timestamp,
            )
            yield reading
            time.sleep(1)  # uma leitura por segundo

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServicer_to_server(SensorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("[Sensor] Servidor gRPC iniciado na porta 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
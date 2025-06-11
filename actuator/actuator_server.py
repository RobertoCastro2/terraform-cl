import time
from concurrent import futures

import grpc
import actuator_pb2
import actuator_pb2_grpc

class ActuatorServicer(actuator_pb2_grpc.ActuatorServicer):
    def Execute(self, request_iterator, context):
        for cmd in request_iterator:
            sensor_id = cmd.sensor_id
            avg = cmd.average
            # Lógica simples de atuação: ligar se média > 25°C
            turn_on = avg > 25.0
            timestamp = int(time.time() * 1000)
            response = actuator_pb2.ActuationCommand(
                sensor_id=sensor_id,
                average=avg,
                timestamp=timestamp,
                turn_on=turn_on,
            )
            print(f"[Actuator] Sensor {sensor_id}: avg={avg:.2f} -> {'ON' if turn_on else 'OFF'}")
            yield response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    actuator_pb2_grpc.add_ActuatorServicer_to_server(ActuatorServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("[Actuator] Servidor gRPC iniciado na porta 50053")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
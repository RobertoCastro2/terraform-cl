#!/usr/bin/env python3
import time
from concurrent import futures
import grpc

import processor_pb2
import processor_pb2_grpc

class ProcessorServicer(processor_pb2_grpc.ProcessorServicer):
    def ProcessReadings(self, request_iterator, context):
        count = 0
        total = 0.0
        sensor_id = None
        for temp in request_iterator:
            if sensor_id is None:
                sensor_id = temp.sensor_id
            total += temp.value
            count += 1
            average = total / count
            timestamp = int(time.time() * 1000)
            processed = processor_pb2.ProcessedData(
                sensor_id=sensor_id,
                average=average,
                timestamp=timestamp,
            )
            yield processed


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    processor_pb2_grpc.add_ProcessorServicer_to_server(ProcessorServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print('[Processor] Servidor gRPC iniciado na porta 50052')
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
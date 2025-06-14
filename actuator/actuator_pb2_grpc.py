# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import actuator_pb2 as actuator__pb2

GRPC_GENERATED_VERSION = '1.73.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in actuator_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ActuatorStub(object):
    """Serviço de Atuação
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Execute = channel.stream_stream(
                '/actuator.Actuator/Execute',
                request_serializer=actuator__pb2.ActuationCommand.SerializeToString,
                response_deserializer=actuator__pb2.ActuationCommand.FromString,
                _registered_method=True)


class ActuatorServicer(object):
    """Serviço de Atuação
    """

    def Execute(self, request_iterator, context):
        """Recebe stream de ProcessedData (média) e retorna confirmações
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ActuatorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Execute': grpc.stream_stream_rpc_method_handler(
                    servicer.Execute,
                    request_deserializer=actuator__pb2.ActuationCommand.FromString,
                    response_serializer=actuator__pb2.ActuationCommand.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'actuator.Actuator', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('actuator.Actuator', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Actuator(object):
    """Serviço de Atuação
    """

    @staticmethod
    def Execute(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/actuator.Actuator/Execute',
            actuator__pb2.ActuationCommand.SerializeToString,
            actuator__pb2.ActuationCommand.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

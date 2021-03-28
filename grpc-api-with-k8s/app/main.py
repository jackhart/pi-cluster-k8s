import os
import logging
from absl import app
from absl import flags
from concurrent import futures
import socket
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor import exceptions

import info_pb2
import info_pb2_grpc


FLAGS = flags.FLAGS
flags.DEFINE_string('port', os.environ.get("PORT", "localhost:5001"), 'port to listen on')
flags.DEFINE_string('private_key', '', 'the private key for SSL/TLS setup')
flags.DEFINE_string('certificate_chain', '', 'the cert for SSL/TLS setup')


class InfoService(info_pb2_grpc.InfoServiceServicer):

    def __init__(self):
        # self.host_name = "POMPOM"
        self.host_name = socket.gethostname()

    def name_info(self, request, context):
        """Return DNS name of the current node.
        """
        try:
            name = info_pb2.NodeNameResponse.Name.Value(self.host_name.upper())
        except Exception as ex:
            raise exceptions.NotFound(str(ex))

        return info_pb2.NodeNameResponse(name=name)


def build_ssl_credentials(private_key, certificate_chain):
    with open(private_key, 'rb') as f:
        private_key = f.read()
    with open(certificate_chain, 'rb') as f:
        certificate_chain = f.read()
    return grpc.ssl_server_credentials(((private_key, certificate_chain,),))


def main(argv):

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                         interceptors=[ExceptionToStatusInterceptor()])
    info_pb2_grpc.add_InfoServiceServicer_to_server(InfoService(), server)

    if FLAGS.private_key and FLAGS.certificate_chain:
        credentials = build_ssl_credentials(FLAGS.private_key, FLAGS.certificate_chain)
        server.add_secure_port(str(FLAGS.port), credentials)
    else:
        server.add_insecure_port(str(FLAGS.port))

    logging.log(level=logging.INFO, msg="server starting")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(main)

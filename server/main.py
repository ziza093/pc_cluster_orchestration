import grpc
from concurrent import futures
from proto import main_pb2
from proto import main_pb2_grpc
import logging
import uuid
from services.servicer import IdmServicer
from services import tokens 

class LoginService(main_pb2_grpc.LoginServicer):
    def __init__(self):    
        self.idmServicer = IdmServicer()

    def Login(self, request, context):
        return self.idmServicer.auth(request, context)

    def ListAccounts(self, request, context):
         return self.idmServicer.listAccounts(request, context)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    main_pb2_grpc.add_LoginServicer_to_server(LoginService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started!")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.stop(grace=5).wait()
        print("Server stopped.")


if __name__ == "__main__":

    if not tokens.JWT_SECRET:
            raise SystemExit(
                "Create JWT_SECRET to be able to start."
            )
    serve() 
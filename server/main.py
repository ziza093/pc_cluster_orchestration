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

    def CreateAccount(self, request, context):
         return self.idmServicer.createAccount(request, context)

    def DeactivateAccount(self, request, context):
         return self.idmServicer.deactivateAccount(request, context)

    def ActivateAccount(self, request, context):
         return self.idmServicer.activateAccount(request, context)

    def ValidateToken(self, request, context):
         return self.idmServicer.validateToken(request, context)

    def DestroyToken(self, request, context):
         return self.idmServicer.destroyToken(request, context)

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
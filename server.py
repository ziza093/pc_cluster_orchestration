import grpc
from concurrent import futures
import main_pb2
import main_pb2_grpc
import logging
import uuid

import databases as db
from auth_service import auth
from login_service.login import LoginUser
from login_service.listAccounts import ListUserAccounts


class LoginService(main_pb2_grpc.LoginServicer):
    def __init__(self):    
        self.loginUser = LoginUser()
        self.listUserAccounts = ListUserAccounts()

    def Login(self, request, context):
        return self.loginUser.login(request, context)

    def ListAccounts(self, request, context):
         return self.listUserAccounts.listAccounts(request, context)

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

    if not auth.JWT_SECRET:
            raise SystemExit(
                "Create JWT_SECRET to be able to start."
            )
    serve() 
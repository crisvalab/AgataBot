from flask import Blueprint

class RouterManager():

    def __init__(self, name):
        self.name = name

    def config_routes(self, token_required, throw_request_error) -> Blueprint:
        pass

import cli_handler
import mongo_handler

users = {
        'cli': {'username':'cli', 'password':'cli', 'cli':True, 'handlers':[cli_handler, mongo_handler]},
        'test': {'username':'test', 'password':'test', 'cli':True, 'handlers':[cli_handler]},
        'mongo': {'username':'mongo', 'password':'mongo', 'cli':False, 'handlers':[mongo_handler]},
        }

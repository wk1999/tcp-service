
import cli_handler
import mongo_handler

users = {
        'test': {'username':'test', 'password':'test', 'cli':True, 'handler':cli_handler},
        'mongo': {'username':'mongo', 'password':'mongo', 'cli':False, 'handler':mongo_handler},
        }

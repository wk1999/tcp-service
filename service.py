
import sys
import os

class service:
    def __init__(self, module_name, service_class):
        self._service_path = None
        self._module_name = module_name
        self._service_class = service_class
        self._service = None
    def load(self, service_path):
        if os.path.isdir(service_path):
            self._service_path = os.path.abspath(service_path)
            sys.path.append(self._service_path)
            try:
                module = __import__(self._module_name)
                if os.path.dirname(module.__file__) != self._service_path:
                    print('module loaded but in wrong directory %s, should in %s'
                            %(os.path.dirname(module.__file__), self._service_path))
                    return False
            except Exception, e:
                print('load service module error', self._module_name)
                print str(e)
                return False
            
            if hasattr(module, self._service_class):
                service_class = getattr(module, self._service_class)
                self._service = service_class()
            else:
                print('create service instance error', self._service_class)
                return False

            return True
        else:
            print('service path not exist', service_path)
            return False
    def name(self):
        if self._service:
            return self._service.name()
    def addr(self):
        if self._service:
            return self._service.addr()
    def port(self):
        if self._service:
            return self._service.port()
    def create_session(self, *args, **kwargs):
        if self._service:
            return self._service.create_session(*args, **kwargs)
    def is_frame(self, *args, **kwargs):
        if self._service:
            return self._service.is_frame(*args, **kwargs)
        return False
    def user_data(self):
        if self._service:
            return self._service.user_data()

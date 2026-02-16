from .container import Container

class AppFactory:
    _registry = {}

    @classmethod
    def register(cls, dependency):
        def decorator(builder):
            cls._registry[dependency] = builder
            return builder
        return decorator

    def __init__(self, container: Container):
        self.container = container
        self._instances = {}

    def create(self, dependency):
        if dependency in self._instances:
            return self._instances[dependency]

        builder = self._registry.get(dependency)
        if not builder:
            raise ValueError(f"No builder registered for {dependency}")

        instance = builder(self)
        self._instances[dependency] = instance
        return instance
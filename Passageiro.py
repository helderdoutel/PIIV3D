class Passageiro(object):

    def __init__(self, hora_chegada=None, hora_elevador=None, vertices=None):
        """."""
        self.hora_chegada = hora_chegada
        self.hora_elevador = hora_elevador
        self.vertices = None

    def get_hora_chegada(self):
        """."""
        return self.hora_chegada

    def set_hora_chegada(self, hora_chegada):
        """."""
        self.hora_chegada = hora_chegada

    def get_hora_elevador(self):
        """."""
        return self.hora_elevador

    def set_hora_elevador(self, hora_elevador):
        """."""
        self.hora_elevador = hora_elevador

    def get_vertices(self):
        """."""
        return self.vertices

    def set_vertices(self, vertices):
        """."""
        self.vertices = vertices

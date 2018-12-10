class Passageiro(object):

    def __init__(self, id_passageiro, hora_chegada=None, hora_elevador=None, vertices=None):
        """."""
        self.hora_chegada = hora_chegada
        self.hora_elevador = hora_elevador
        self.vertices = None
        self.elevador = None
        self.id_passageiro = id_passageiro
        self.posicao = None

    def get_id(self):
        """."""
        return self.id_passageiro

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

    def esperando(self, hora_atual):
        """."""
        return (self.get_hora_chegada() <= hora_atual and
                self.get_hora_elevador() is None)

    def get_elevador(self):
        """."""
        return self.elevador

    def set_elevador(self, elevador):
        """."""
        self.elevador = elevador

    def andando(self):
        """."""
        return (self.get_elevador() is not None and
                self.get_hora_elevador() is None)

    def get_centro_objeto(self):
        """."""
        maior_x = max([i[0] for i in self.get_vertices()])
        menor_x = min([i[0] for i in self.get_vertices()])
        centro_x = menor_x + ((maior_x - menor_x) / 2)

        maior_y = max([i[1] for i in self.get_vertices()])
        menor_y = min([i[1] for i in self.get_vertices()])
        centro_y = menor_y + ((maior_y - menor_y) / 2)

        maior_z = max([i[2] for i in self.get_vertices()])
        menor_z = min([i[2] for i in self.get_vertices()])
        centro_z = menor_z + ((maior_z - menor_z) / 2)
        return centro_x, centro_y, centro_z

    def get_posicao(self):
        """."""
        return self.posicao

    def set_posicao(self, posicao):
        """."""
        self.posicao = posicao

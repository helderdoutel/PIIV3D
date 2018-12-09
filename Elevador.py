class Elevador(object):

    def __init__(self):
        """Construtor."""
        self.ultima_partida = None
        self.tempo_viagem = None
        self.passageiros = []
        self.quebrado_hora = None
        self.viagens = 0
        self.vertices = None

    def get_ultima_partida(self):
        """."""
        return self.ultima_partida

    def set_ultima_partida(self, ultima_partida):
        """."""
        self.ultima_partida = ultima_partida

    def get_tempo_viagem(self):
        """."""
        return self.tempo_viagem

    def set_tempo_viagem(self, tempo_viagem):
        """."""
        self.tempo_viagem = tempo_viagem

    def get_passageiros(self):
        """."""
        return self.passageiros

    # def set_passageiros(self, passageiros):
    #     """."""
    #     self.passageiros = passageiros

    def get_quebrado_hora(self):
        """."""
        return self.quebrado_hora

    def set_quebrado_hora(self, quebrado_hora):
        """."""
        self.quebrado_hora = quebrado_hora

    def get_viagens(self):
        """."""
        return self.viagens

    def set_viagens(self):
        """."""
        self.viagens = self.viagens + 1

    def get_vertices(self):
        """."""
        return self.vertices

    def set_vertices(self, vertices):
        """."""
        self.vertices = vertices

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

    def em_viagem(self, hora_atual):
        """."""
        return ((self.get_ultima_partida() + self.get_tempo_viagem()) > hora_atual)

    def add_passageiro(self, id_passageiro):
        """."""
        self.passageiros.append(id_passageiro)

    def zerar_passageiro(self):
        """."""
        self.passageiros = []

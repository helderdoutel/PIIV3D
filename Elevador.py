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

    def set_passageiros(self, passageiros):
        """."""
        self.passageiros = passageiros

    def get_quebrado_hora(self):
        """."""
        return self.quebrado_hora

    def set_quebrado_hora(self, quebrado_hora):
        """."""
        self.quebrado_hora = quebrado_hora

    def get_viagens(self):
        """."""
        return self.viagens

    def set_viagens(self, viagens):
        """."""
        self.viagens = viagens

    def get_vertices(self):
        """."""
        return self.vertices

    def set_vertices(self, vertices):
        """."""
        self.vertices = vertices

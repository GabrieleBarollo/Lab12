from copy import deepcopy

import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self._map_difficolta = {"facile": 1,
                                "media": 1.5,
                                "difficile": 2}

        self._map_rifugi = {}
        self._lista_rifugi = []
        self.G = nx.Graph()

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self._lista_rifugi = DAO.read_all_rifugi()
        for rifugio in self._lista_rifugi:
            self._map_rifugi[rifugio.id] = rifugio

        self._lista_connessioni = DAO.read_connessioni(year)
        for connessione in self._lista_connessioni:
            l = [(connessione.id_rifugio1, connessione.id_rifugio2, float(connessione.distanza)*self._map_difficolta[connessione.difficolta])]
            self.G.add_weighted_edges_from(l)





    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        self.minimo = float("inf")
        self.massimo = float("-inf")
        for u, v in self.G.edges():
            peso = self.G.get_edge_data(u, v)['weight']
            if peso < self.minimo:
                self.minimo = peso
            elif peso > self.massimo:
                self.massimo = peso

        return self.minimo, self.massimo

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        self.s = soglia
        count_minori = 0
        count_maggiori = 0
        for u, v in self.G.edges():
            peso = self.G.get_edge_data(u, v)['weight']
            if peso < soglia:
                count_minori += 1
            elif peso > soglia:
                count_maggiori += 1

        return count_minori, count_maggiori

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    """PARTE SENZA RICORSIONE"""

    def search_minimum_path(self):
        edges_to_remove = []
        self.G_filtrato = self.G.copy()
        for u, v in self.G.edges():
            peso = self.G.get_edge_data(u, v)['weight']
            if peso <= self.s:
                edges_to_remove.append((u, v))

        self.G_filtrato.remove_edges_from(edges_to_remove)
        self.soluzione = None
        minimo = float("inf")
        lista_nodi = list(self.G_filtrato.nodes())

        for a in range(0, len(lista_nodi)):
            for b in range(a+1, len(lista_nodi)):
                nodo_partenza = lista_nodi[a]
                nodo_arrivo = lista_nodi[b]

                try:

                    peso_totale = nx.shortest_path_length(self.G_filtrato, nodo_partenza, nodo_arrivo, weight='weight')
                    possibile_soluzione = nx.shortest_path(self.G_filtrato, nodo_partenza, nodo_arrivo, weight='weight')
                    if len(possibile_soluzione) == 3 and peso_totale < minimo:
                        minimo = peso_totale
                        self.soluzione = possibile_soluzione

                except nx.NetworkXNoPath:
                    continue

        return self.soluzione

    """
    PARTE CON LA RICORSIONE
    def search_minimum_path(self):
        edges_to_remove = []
        self.G_filtrato = self.G.copy()
        for u, v in self.G.edges():
            peso = self.G.get_edge_data(u, v)['weight']
            if peso <= self.s:
                edges_to_remove.append((u, v))

        self.G_filtrato.remove_edges_from(edges_to_remove)

        self.minimo_corrente = float("inf")
        self.soluzione = []
        self.ricorsione(self.G_filtrato, [], 0)
        #print(self.soluzione)


    def ricorsione(self, grafo, possibile_soluzione, valore_weight):

        if len(possibile_soluzione) == 3:
            #print(possibile_soluzione, self.calcolo_min(possibile_soluzione))
            if valore_weight < self.minimo_corrente:
                self.minimo_corrente = valore_weight
                self.soluzione = deepcopy(possibile_soluzione)


        else:
            for tupla_nodi in grafo.edges():
                for nodo_vicino in grafo.neighbors(tupla_nodi[1]):
                    if nodo_vicino != tupla_nodi[0] and nodo_vicino != tupla_nodi[1]:
                        possibile_soluzione.append(tupla_nodi[0])
                        possibile_soluzione.append(tupla_nodi[1])
                        possibile_soluzione.append(nodo_vicino)
                        #print(possibile_soluzione)
                        valore_weight = self.calcolo_min(possibile_soluzione)
                        self.ricorsione(self.G_filtrato, possibile_soluzione, valore_weight)
                        possibile_soluzione.clear()




    def calcolo_min(self, possibile_soluzione):
        s = self.G_filtrato.get_edge_data(possibile_soluzione[0], possibile_soluzione[1])['weight'] + self.G_filtrato.get_edge_data(possibile_soluzione[1], possibile_soluzione[2])['weight']
        return s
    """





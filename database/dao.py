from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:

    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO

    @staticmethod
    def read_all_rifugi():
        results = []
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM rifugio"
        cursor.execute(query)
        for row in cursor:
            results.append(Rifugio(row["id"], row["nome"], row["localita"],
                                   row["altitudine"], row["capienza"], row["aperto"]))

        cursor.close()
        cnx.close()
        return results

    @staticmethod
    def read_connessioni(year):
        results = []
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT id_rifugio1, id_rifugio2, distanza, difficolta, anno
                   FROM connessione
                   WHERE anno <= %s"""
        cursor.execute(query, (year,))
        for row in cursor:
            results.append(Connessione(row["id_rifugio1"], row["id_rifugio2"], row["distanza"],
                                   row["difficolta"], row["anno"]))

        cursor.close()
        cnx.close()
        return results




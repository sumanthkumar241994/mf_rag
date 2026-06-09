import uuid

import psycopg2
from pgvector.psycopg2 import register_vector


class PostgresWriter:

    def __init__(self):

        self.conn = psycopg2.connect(
            host="localhost",
            port=6543,
            database="postgres",
            user="postgres",
            password="f.RD6->Buk4lmgsa_3:I867~hqbp"
        )

        register_vector(self.conn)

    def save_chunks(self, chunks):

        query = """
        INSERT INTO document_chunks
        (
            chunk_id,
            scheme_name,
            document_type,
            section_name,
            semantic_type,
            chunk_text,
            embedding
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s
        )
        """

        with self.conn.cursor() as cur:

            for chunk in chunks:

                cur.execute(
                    query,
                    (
                        str(uuid.uuid4()),
                        chunk["scheme_name"],
                        chunk["document_type"],
                        chunk["section_name"],
                        chunk["semantic_type"],
                        chunk["chunk_text"],
                        chunk["embedding"]
                    )
                )

        self.conn.commit()

    def close(self):
        self.conn.close()
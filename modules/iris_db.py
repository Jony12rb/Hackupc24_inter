import os, pandas as pd
from sqlalchemy import create_engine, text
from openai import OpenAI

EMBEDDINGS_DIM = 1536


class IrisDB:
    def __init__(
            self, 
            username: str = 'demo',
            password: str = 'demo',
            hostname: str = os.getenv('IRIS_HOSTNAME', 'localhost'),
            port: str = '1972',
            namespace: str = 'USER',
            Openai_client: OpenAI = None,
        ):
        self._CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"
        self.engine = create_engine(self._CONNECTION_STRING)
        
        self.client = Openai_client

    def get_embedding(self, txt, model="text-embedding-3-small"):
        txt = txt.replace("\n", " ")
        return self.client.embeddings.create(input = [txt], model=model, dimensions=EMBEDDINGS_DIM).data[0].embedding
    
    def get_batch_embedding(self, texts, model="text-embedding-3-small"):
        return [e.embedding for e in self.client.embeddings.create(input = texts, model=model).data]

    def table_exists(self, name: str = 'gallery_images'):
        with self.engine.connect() as conn:
            with conn.begin():
                sql = f"""SELECT * FROM {name}"""
                try:
                    conn.execute(text(sql))
                    return True
                except Exception as e:
                    return False

    def init_table(self, name: str = 'gallery_images'):
        with self.engine.connect() as conn:
            with conn.begin():
                sql = f"""DROP TABLE IF EXISTS {name}"""
                result = conn.execute(text(sql))
                
                sql = f"""
                        CREATE TABLE {name} (
                        path VARCHAR(255),
                        description VARCHAR(2000),
                        description_vector VECTOR(DOUBLE, {EMBEDDINGS_DIM})
                )
                        """
                result = conn.execute(text(sql))
    
    def insert_df_to_table(self, df: pd.DataFrame, name: str = 'gallery_images'):
        assert 'image_path' in df.columns, "image_path column is missing"
        assert 'description' in df.columns, "description column is missing"

        if 'description_vector' not in df.columns:
            df['description_vector'] = self.get_batch_embedding(df['description'].tolist())
        
        with self.engine.connect() as conn:
            with conn.begin():
                for index, row in df.iterrows():
                    sql = text(f"""
                        INSERT INTO {name}
                        (path, description, description_vector)
                        VALUES (:path, :description, TO_VECTOR(:description_vector))
                    """)
                    conn.execute(sql, {
                        'path': row['image_path'],
                        'description': row['description'],
                        'description_vector': str(row['description_vector'])
                    })

    def description_search(self, query: str, top_n: int, name: str = 'gallery_images'):
        embedding = self.get_embedding(query)
        with self.engine.connect() as conn:
            with conn.begin():
                sql = text(f"""
                    SELECT TOP {top_n} * FROM {name}
                    ORDER BY VECTOR_DOT_PRODUCT(description_vector, TO_VECTOR(:search_vector)) DESC
                """)

                results = conn.execute(sql, {'search_vector': str(embedding)}).fetchall()
        return pd.DataFrame(results)


if __name__ == '__main__':
    OPENAI_API_KEY = open('OPENAI_API_KEY.txt').read().strip()
    iris = IrisDB(Openai_client = OpenAI(api_key=OPENAI_API_KEY))

    if not iris.table_exists():
        # df = pd.DataFrame({
        #     'image_path': ['image1.jpg', 'image2.jpg', 'image3.jpg'],
        #     'description': ['a cat', 'a dog', 'a car']
        # })
        df = pd.read_csv('Data/version2.csv')
        df.columns = ['image_path', 'description']

        iris.init_table()
        iris.insert_df_to_table(df)

    description_search = "music"
    results = iris.description_search(description_search, top_n=3)
    # limit prints of pd.DataFrame to 240 characters
    pd.set_option('display.max_colwidth', 240)
    print(results[['path', 'description']])

    # import matplotlib.pyplot as plt
    # from PIL import Image
    # for index, row in results.iterrows():
    #     img = Image.open(row['path'])
    #     plt.imshow(img)
    #     plt.show()
    #     print(f"Description: {row['description']}\n\n")

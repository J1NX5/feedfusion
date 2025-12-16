import sqlite3

class DBManager:
    def __init__(self):
        self.__db_path: str = "data/data.db"
        self.__conn = self._create_connection(self.__db_path)
        self._create_table()

    def _create_connection(self, db_file):
        connection = sqlite3.connect(db_file)
        return connection
    

    def _create_table(self):
        cursor = self.__conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rss_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rss_id TEXT NOT NULL,
                title TEXT NOT NULL,
                link TEXT NOT NULL,
                published TEXT NOT NULL,
                author TEXT NOT NULL,
                source TEXT NOT NULL,
                active INTEGER NOT NULL
            ); 
        ''')
        cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS unique_rss_id_and_source ON rss_table(rss_id, source);
        ''')
        return self.__conn.commit()

    def insert_feed(
        self, 
        rss_id: str, 
        title: str,
        link: str,
        published: str,
        author: str,
        source: str,
        active: int
        ):
        cursor = self.__conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO rss_table(
                rss_id,
                title,
                link,
                published,
                author,
                source,
                active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?);
            ''', (  
                    rss_id,
                    title,
                    link,
                    published,
                    author,
                    source,
                    active
                )
        ) 
        return self.__conn.commit()

    def check_entry_exist(
        self,
        rss_id: str,
        ):
        cursor = self.__conn.cursor()
        cursor.execute(
        "SELECT 1 FROM rss_table WHERE rss_id = ? LIMIT 1;",
        (rss_id,)
        )
        return cursor.fetchone()

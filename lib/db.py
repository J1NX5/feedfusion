import sqlite3

class DBManager:
    def __init__(self):
        self.__db_path: str = "data.db"
        self.__conn = self._create_connection(self.db_path)
        self._create_table_for_fmp()

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
                summary TEXT NOT NULL,
                link TEXT NOT NULL,
                published TEXT NOT NULL,
                author TEXT NOT NULL,
            ); 
        ''')
        cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS unique_symbol_date ON rss_table(rss_id);
        ''')
        return self.__conn.commit()

    # A func which get the earning report in delay of 1 day
    def insert_feed(
        self, 
        rss_id: str, 
        title: str,
        summary: str,
        link: str,
        published: str,
        author: str
        ):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO rss_table(
                rss_id,
                title,
                summary,
                link,
                published,
                author
            )
            VALUES (?, ?, ?, ?, ?, ?, );
            ''', (  
                    rss_id,
                    title,
                    summary,
                    link,
                    published,
                    author 
                )
        ) 
        return self.__conn.commit()
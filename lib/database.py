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
                feed_text TEXT DEFAULT NULL,
                link TEXT NOT NULL,
                published TEXT NOT NULL,
                author TEXT NOT NULL,
                source TEXT NOT NULL,
                dom TEXT DEFAULT NULL,
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

    def get_active_urls_without_text(self):
        cursor = self.__conn.cursor()
        cursor.execute("SELECT * FROM rss_table WHERE feed_text is NULL AND active = 1 LIMIT 5;")
        return cursor.fetchall()

    def get_urls_without_dom(self):
        cursor = self.__conn.cursor()
        cursor.execute("SELECT * FROM rss_table WHERE dom is NULL LIMIT 5;")
        return cursor.fetchall()

    def update_feed_text_by_url(self, feed_text, feed_url):
        cursor = self.__conn.cursor()
        cursor.execute(
            "UPDATE rss_table SET feed_text = ?, active = 0  WHERE link = ?;",
            (feed_text, feed_url)
        )
        return self.__conn.commit()

    def update_dom_by_url(self, dom_url, feed_url):
        cursor = self.__conn.cursor()
        cursor.execute(
            "UPDATE rss_table SET dom = ?, active = 0  WHERE link = ?;",
            (dom_url, feed_url)
        )
        return self.__conn.commit()

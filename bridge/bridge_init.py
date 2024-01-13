import configparser
from dataclasses import dataclass
from enum import Enum
import sqlite3
from typing import Dict, List, Tuple

import utils


class MetaInfoQuerry(Enum):
    SQLITE = """SELECT
                    m.name AS table_name,
                    p.name AS column_name,
                    p.type AS type
                FROM
                    sqlite_master AS m
                JOIN
                    pragma_table_info(m.name) AS p
                WHERE
                    m.type = 'table';
            """


@dataclass
class BInit:
    """Class that is responsible for creating bridge function args

    Exposes: `prepare_bridge_function_args()`"""

    bql_properties = configparser.ConfigParser()

    def __post_init__(self) -> None:
        self._sanity_check()
        self.test_db()

    @utils.property_file_readability_check
    def _sanity_check(self):
        pass

    def test_db(self):
        """Check if you are able to use the db on the provided details"""
        self.source_type = self.bql_properties.get("source", "source.db.type").lower()
        if self.source_type == "sqlite":
            source_db_path = self.bql_properties.get("source", "source.db.path")
            try:
                self._establish_db_connection(source_db_path)
            except Exception as e:
                print(f"Error during database connection: {e}")

    def prepare_bridge_function_args(self):
        """Creates a meta file for the available function args"""
        if self.source_type == "sqlite":
            tables = self.db.get_tables_meta(query=MetaInfoQuerry.SQLITE.value)
            arg_dir = self.bql_properties.get(section="project", option="args.dir")

            utils.check_file_exist(
                f"{arg_dir}/args",
                onSucces=utils.FileOps.SKIP,
                onFailure=utils.FileOps.CREATE_FILE,
            )
            f = open("data/args", "w")
            print(tables, file=f, flush=True)

    def _establish_db_connection(self, db_path):
        source_db_username = self.bql_properties.get("source", "source.db.username")
        source_db_password = self.bql_properties.get("source", "source.db.password")

        utils.check_file_exist(
            file_path=db_path,
            onSucces=utils.FileOps.SKIP,
            onFailure=utils.FileOps.EXCEPTION,
        )

        auth = (source_db_username, source_db_password)
        self.db = SQLiteDB(db=db_path, auth=auth)

        try:
            self.db.get_connection()
        except ConnectionRefusedError as e:
            print(f"Connection refused: {e}")
        except ConnectionError as e:
            print(f"Unable to get the managed connection: {e}")
        except Exception as e:
            print(f"Unknown exception occurred during establishing the connection: {e}")


@dataclass
class SQLiteDB:
    db: str
    auth: str

    def get_connection(self) -> None:
        self.connection = sqlite3.connect(database=self.db)
        self.cursor = self.connection.cursor()

    def get_tables_meta(self, query: str) -> Dict[str, Dict[str, str]]:
        self.cursor.execute(query)
        meta: List[Tuple[str, str, str]] = self.cursor.fetchall()
        data: Dict[str, Dict[str, str]] = {}

        for table, column, dtype in meta:
            if table not in data:
                data[table] = {}
            data[table][column] = dtype
        return data


if __name__ == "__main__":
    b = BInit()
    b.prepare_bridge_function_args()

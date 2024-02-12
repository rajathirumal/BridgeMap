import ast
import configparser
from dataclasses import dataclass
import os
import re
import utils


@dataclass
class Analyzer:
    source: str
    property: configparser.ConfigParser

    def __post_init__(self):
        self.code: str = utils.read_file(path=self.source)
        self.property
        # self.parse()
        print(self.generate_sql(self.code))

    def generate_sql(self, query):
        parts = query.split("|")
        columns = "*"
        if len(parts) < 2 or len(parts) > 3:
            raise ValueError("Invalid query format")

        action, table = parts[0], parts[1]
        columns = action.split()[1].lower()
        if len(action.split(" ")) < 2:
            raise ValueError("get expects atleast one selector")
        if action.split()[0].lower() != "get":
            raise ValueError("Unsupported action. Only 'get' is supported.")
        try:
            if columns == "all" or "*":
                columns = self.get_columns(table)
        except IndexError:
            columns = "*"

        columns_to_select = "*"
        conditions = ""

        if len(parts) == 3:
            operators = {"eq": "==", "gt": ">"}
            conditions = parts[2]
            conditions_parts = conditions.split()

            if len(conditions_parts) != 3:
                raise ValueError("Invalid conditions format")
            columns_to_select, operator, value = conditions_parts
            if operator not in list(operators.keys()):
                raise SyntaxError(f"{operator} not valid")
            if columns_to_select not in columns:
                raise KeyError(f"No such column {columns_to_select} in {table}")
            condition = f"{columns_to_select} {operators.get(operator,'')} {value}"

            return f"SELECT {list(columns)} FROM {table} WHERE {condition}"

        if conditions:
            sql_statement += f" WHERE {columns_to_select} {operator} {value}"

        return sql_statement

    def get_columns(self, table) -> list:
        file_content: dict = ast.literal_eval(utils.read_file(path="data/args"))
        return file_content[table].keys()


@dataclass
class BCompile:
    source: str
    bql_properties = configparser.ConfigParser()

    def __post_init__(self):
        self.sanity_check()
        self.analyse()

    @utils.property_file_readability_check
    def sanity_check(self):
        # Check for the .bql file
        try:
            utils.check_file_exist(
                file_path=self.source,
                onSucces=utils.FileOps.SKIP,
                onFailure=utils.FileOps.EXCEPTION,
            )
        except Exception as e:
            raise Exception(str(e))

        # check if the bql project is initiated
        try:
            utils.check_file_exist(
                file_path=self.bql_properties.get("project", "args.dir")
                + "/"
                + self.bql_properties.get("project", "args.file"),
                onSucces=utils.FileOps.SKIP,
                onFailure=utils.FileOps.EXCEPTION,
            )
        except Exception as e:
            raise FileNotFoundError("Please run BInit before compiling")

    def analyse(self):
        try:
            Analyzer(self.source, self.bql_properties)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # BCompile(source="file/not/found")
    BCompile(source="examples/SQlite/code/select.bql")

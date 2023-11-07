import configparser
from dataclasses import dataclass
import re
import utils


@dataclass
class Analyzer:
    source: str

    def __post_init__(self):
        self.code: str = utils.read_file(path=self.source)
        self.parse()

    def parse(self):
        code = self.code

        key_words = ["proc", "view", "if", "else", "else-if", "define_table"]
        operator_pattern = r"[=!<>\-+*/\(\)\{\}]"
        string_pattern = r'"[^"\\]*(?:\\.[^"\\]*)*"'
        variable_pattern = r"\b(\w+)\b"

        # Compile regex patterns
        keyword_pattern = re.compile(rf"\b({'|'.join(key_words)})\b")
        operator_regex = re.compile(operator_pattern)
        string_regex = re.compile(string_pattern)
        variable_regex = re.compile(variable_pattern)

        # Find and print matches
        found_matches = False  # Flag to check if any match was found

        matches = []

        ind = []

        # Find all matches and store in a list for filtering
        for match in re.finditer(variable_regex, code):
            matches.append((match.group(), match.start(), match.end()))

        # Iterate through matches and print only non-keyword variable matches
        for variable, start, end in matches:
            # Check if the variable is not a keyword
            if variable not in key_words:
                print(f"Variable: {variable} at ({start}, {end})")

                found_matches = True

        for match in re.finditer(keyword_pattern, code):
            print(f"Keyword: {match.group()} at ({match.start()}, {match.end()})")
            found_matches = True

        for match in re.finditer(operator_regex, code):
            print(f"Operator: {match.group()} at ({match.start()}, {match.end()})")
            found_matches = True

        if not found_matches:
            print("Variable: (entire code content)")

        print(self.code)
        print(ind)


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
            Analyzer(self.source)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # BCompile(source="file/not/found")
    BCompile(source="examples/SQlite/test.bql")

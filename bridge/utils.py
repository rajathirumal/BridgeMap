from enum import Enum
from functools import wraps
from chardet.universaldetector import UniversalDetector
import os


def detect_encoding(file_path):
    """Predicts the encodig of the file using `chardet` module"""
    detector = UniversalDetector()
    with open(file_path, "rb") as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result["encoding"]


def property_file_readability_check(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        property_file = "conf/BQL.properties"
        if os.path.exists(property_file):
            try:
                with open(
                    property_file, mode="r", encoding=detect_encoding(property_file)
                ) as f:
                    # Looks like you can fetch data from a property file only if you read it once.
                    self.bql_properties.read_file(f)
            except Exception as e:
                raise Exception(
                    f"Unable to read the property file: {property_file}"
                ) from e
            finally:
                f.close()
        else:
            raise FileNotFoundError(f"Property file not found: {property_file}")
        result = func(self, *args, **kwargs)
        return result

    return wrapper


class FileOps(Enum):
    CREATE_FILE = "create"
    SKIP = "skip"
    EXCEPTION = "exception"


def check_file_exist(file_path: str, onSucces: FileOps, onFailure: FileOps) -> None:
    if os.path.exists(file_path):
        if onSucces == FileOps.CREATE_FILE:
            raise Exception(f"{file_path} already exists")
        elif onSucces == FileOps.EXCEPTION:
            raise Exception(f"Invalid operation when the file exists at {file_path}")

    else:
        if onFailure == FileOps.CREATE_FILE:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w"):
                pass  # Create the file
        elif onFailure == FileOps.EXCEPTION:
            raise FileNotFoundError(f"File not found at {file_path}")


def read_file(path: str) -> str:
    path = os.path.abspath(path)
    try:
        with open(path, mode="r", encoding=detect_encoding(path)) as f:
            contents = f.read().replace("\n", "").strip()
            # contents = list(filter(None, f.read().strip().split("\n")))
            # contents = [item.strip() for item in contents]
            return contents
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error reading file: {e}"

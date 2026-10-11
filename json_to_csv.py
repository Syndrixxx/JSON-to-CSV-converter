import argparse
import json
import csv
import sys


def ensure_extension(path: str, extension: str) -> str:
    """Return the path with the given extension, adding it if it is missing.

    Args:
        path: File path or name provided by the user.
        extension: Required extension including the dot (e.g. ".csv").

    Returns:
        The original path if it already ends with the extension (case-insensitive),
        otherwise the path with the extension appended.
    """
    if path.lower().endswith(extension):
        return path
    return path + extension

def get_data_from_json(path: str) -> list[dict] | dict | None:
    """Load and return the contents of a JSON file, or None if loading fails.

    Args:
        path: Path to the input .json file.

    Returns:
        Parsed JSON data (list of dicts or a single dict), or None on error.
    """
    try:
        with open(path, mode="r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"Error: file '{path}' was not found.")
    except PermissionError:
        print(f"Error: no permission to read '{path}'.")
    except json.JSONDecodeError as error:
        print(f"Error: '{path}' is not a valid JSON file ({error}).")
    except UnicodeDecodeError as error:
        print(f"Error: '{path}' could not be decoded as UTF-8 ({error}).")
    except OSError as error:
        print(f"Error: could not read '{path}' ({error}).")
    except Exception as error:
        print(f"Unexpected error while reading '{path}': {error!r}")
    return None

def put_data_in_csv(data: list[dict] | dict, path: str) -> bool:
    """Write JSON-like data to a CSV file and return whether it succeeded.

    Args:
        data: A list of dicts (or a single dict) to be written; keys of the
            first dict are used as the CSV header.
        path: Path to the output .csv file.

    Returns:
        True if the file was written successfully, False otherwise.
    """
    if not data:
        print("Data to convert are empty. No .csv file was created or changed.")
        return False
    if isinstance(data, dict):
        data = [data]

    try:
        with open(path, mode="w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.DictWriter(csv_file, delimiter= ";", fieldnames=data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(data)
        return True
    except PermissionError:
        print(f"Error: no permission to write to '{path}' (is it open in another program?).")
    except AttributeError:
        print("Error: data must be a dict or a list of dicts.")
    except ValueError as error:
        print(f"Error: data have inconsistent keys ({error}).")
    except OSError as error:
        print(f"Error: could not write to '{path}' ({error}).")
    except Exception as error:
        print(f"Unexpected error while writing '{path}': {error!r}")
    return False

def main() -> None:
    """Parse command-line arguments and convert a JSON file to a CSV file."""
    parser = argparse.ArgumentParser(description="Convert a JSON file to CSV.")
    parser.add_argument("json_file_location", help="Location of .json file or name, if in same directory")
    parser.add_argument("csv_file_location", help="Location of .csv file or name, if in same directory")
    args = parser.parse_args()

    csv_path = ensure_extension(args.csv_file_location, ".csv")
    json_path = ensure_extension(args.json_file_location, ".json")

    input_data = get_data_from_json(json_path)
    if input_data is None:
        sys.exit(1)

    if not put_data_in_csv(input_data, csv_path):
        sys.exit(1) 

if __name__ == "__main__":
    main()

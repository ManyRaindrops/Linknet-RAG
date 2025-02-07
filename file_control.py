# Programmed with the help of AI. This is part of stage one of the project: learning the material.

import csv
import os
import glob
from typing import List

class FileManager:
    def __init__(self):
        # Initialize a dictionary to map file extensions to their handler methods
        self.file_handlers = {
            'txt': self._handle_text_file,
            'csv': self._handle_csv_file
        }

    def open_file(self, file_path, mode):
        # Get the file extension using os.path.splitext
        file_extension = os.path.splitext(file_path)[1][1:]  # Remove the leading dot
        if file_extension in self.file_handlers:
            try:
                # Call the appropriate handler method
                return self.file_handlers[file_extension](file_path, mode)
            except FileNotFoundError:
                raise FileNotFoundError(f"The file '{file_path}' does not exist.")
            except Exception as e:
                raise RuntimeError(f"An error occurred while opening the file: {e}")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    @staticmethod
    def _handle_text_file(file_path, mode):
        # Open and return a text file
        return open(file_path, mode)

    @staticmethod
    def _handle_csv_file(file_path, mode):
        # Open and return a CSV file with newline='' to handle newlines correctly
        return open(file_path, mode, newline='')

    @staticmethod
    def read_file(file):
        """Read and return the content of a file."""
        try:
            return file.read()
        except Exception as e:
            raise IOError(f"An error occurred while reading the file: {e}")

    @staticmethod
    def write_to_file(file, content):
        """Write content to a file."""
        try:
            file.write(content)
        except Exception as e:
            raise IOError(f"An error occurred while writing to the file: {e}")

    @staticmethod
    def read_csv(file):
        """Read and return the content of a CSV file as a list of rows."""
        try:
            reader = csv.reader(file)
            return list(reader)
        except Exception as e:
            raise IOError(f"An error occurred while reading the CSV file: {e}")

    @staticmethod
    def write_to_csv(file, rows):
        """Write rows to a CSV file."""
        try:
            writer = csv.writer(file)
            writer.writerows(rows)
        except Exception as e:
            raise IOError(f"An error occurred while writing to the CSV file: {e}")

    @staticmethod
    def create_file(file_path):
        """Create an empty file."""
        try:
            with open(file_path, 'w'):
                pass  # File is created and closed automatically
            return f"File '{file_path}' created successfully."
        except Exception as e:
            raise IOError(f"An error occurred while creating the file: {e}")

    @staticmethod
    def list_files(path: str, pattern: str) -> List[str]:
        try:
            # Call the function to list files matching the specified pattern in the given folder
            files = FileManager.list_files_with_glob(path, pattern)
            return files
        except ValueError as e:
            # If a ValueError is raised (e.g., invalid directory), print the error message
            print(e)
            """ALERT, WHAT TO DO IF ERROR??? return an exit or something?"""

    @staticmethod
    def list_files_with_glob(folder_path: str, file_pattern: str = '*') -> List[str]:
        """
        Lists all files in the given folder matching the file pattern.

        :param folder_path: Path to the folder containing the files
        :param file_pattern: Pattern to match files (e.g., '*.txt' for text files)
        :return: List of file paths
        :raises ValueError: If the folder_path is not a valid directory
        """
        # Check if the folder path is a valid directory
        if not os.path.isdir(folder_path):
            raise ValueError(f"The specified path '{folder_path}' is not a valid directory.")

        # Construct the full pattern to match files
        search_pattern = os.path.join(folder_path, file_pattern)

        # Use glob to find all files matching the pattern
        files_list = glob.glob(search_pattern)

        if not files_list:
            print(f"No files found matching the pattern '{file_pattern}' in '{folder_path}'.")

        return files_list

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Handle any cleanup if necessary
        pass


"""
# Example usage
file_manager = FileManager()

# Text file manipulation
text_file = file_manager.open_file('example.txt', 'w')
file_manager.write_to_file(text_file, "Hello, this is a text file.")
file_manager.close_file(text_file)

text_file = file_manager.open_file('example.txt', 'r')
print(file_manager.read_file(text_file))
file_manager.close_file(text_file)

# CSV file manipulation
csv_file = file_manager.open_file('example.csv', 'w')
file_manager.write_to_csv(csv_file, [['Name', 'Age'], ['Alice', 30], ['Bob', 25]])
file_manager.close_file(csv_file)

csv_file = file_manager.open_file('example.csv', 'r')
print(file_manager.read_csv(csv_file))
file_manager.close_file(csv_file)

# Creating a new text file
file_manager.create_file('new_text_file.txt')

# Creating a new CSV file
file_manager.create_file('new_csv_file.csv')
"""

class FileCleaner:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = self.identify_file_type()

    def identify_file_type(self):
        """Identify the file type based on the file extension."""
        extension = os.path.splitext(self.file_path)[1][1:]  # Get the extension without the dot
        return {
            'md': 'markdown',
            'txt': 'text',
            'csv': 'csv'
        }.get(extension, 'unknown')

    def process_file(self):
        """Direct the input to the corresponding file-type stripping function."""
        process_methods = {
            'markdown': self.strip_markdown,
            'text': self.strip_text,
            'csv': self.strip_csv
        }
        process_method = process_methods.get(self.file_type, self.unsupported_file_type)
        try:
            process_method()
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")

    @staticmethod
    def strip_markdown():
        """Placeholder for markdown stripping process."""
        pass

    @staticmethod
    def strip_text():
        """Placeholder for text stripping process."""
        pass

    @staticmethod
    def strip_csv():
        """Placeholder for CSV stripping process."""
        pass

    @staticmethod
    def unsupported_file_type():
        """Handle unsupported file types."""
        print("Unsupported file type")

    @classmethod
    def clean_files(cls, files):
        """Clean multiple files by processing each one."""
        for file in files:
            try:
                # Create an instance of FileCleaner with the current file path
                file_cleaner = cls(file)  # Use cls to refer to the class itself

                # Call the process_file method to process the file based on its type
                file_cleaner.process_file()

            except Exception as e:
                print(f"An error occurred while processing the file '{file}': {e}")

    """
    Other methods can be implemented for other file types. To extend this class,
    add new entries to the process_methods dictionary in the process_file method
    and implement the corresponding stripping methods.
    """

"""
Say I have a markdown file with lots of syntactical noise. I want to be able to take that mark-down file and remove the syntax so that the sentences are numbered from 1 to the terminating number and so that the titles and headings are placed into a separate file in which they are separated from the sentences, but still associated to the sentences by the numbers. For example, in a text with 10 sentences, heading A could be associated with sentences 1-3, heading B with sentences 4-7, and heading C with sentences 8-10. The result should have sentences split up into into individual rows in a csv file in the second column. The first column is their number.
"""


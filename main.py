# Programmed with the help of AI. This is part of stage one of the project: learning the material.

import file_control as control
import data_collection as data
import ai_sentence_articulation as processing
from nltk.tokenize import sent_tokenize  # Importing the sentence tokenizer from NLTK

def main():
    api_service = 'something'
    ai_model = 'something'
    iterations = 2  # Number of verification iterations
    folder_path = 'path/to/your/ESSAYS'  # Replace with the path to your ESSAYS folder
    file_pattern = '*.txt'  # Pattern to match text files (e.g., all files with a .txt extension)

    # List all files in the specified folder that match the given pattern
    files = control.FileManager.list_files(folder_path, file_pattern)

    all_sentences = []  # List to store all sentences and their associated ideas
    records_file = 'records.csv'  # Name of the records file to track ideas and chunk data

    # Initialize a list to keep track of established ideas
    established_ideas = []

    # Process each file found in the specified directory
    for file in files:
        # Open the file for reading
        with control.FileManager().open_file(file, 'r') as f:
            content = control.FileManager.read_file(f)  # Read the content of the file

            # Split the content into sentences using NLTK's sentence tokenizer
            sentences = sent_tokenize(content)

            # Process each sentence
            for sentence in sentences:
                idea = processing.ConnectProcessor(api_service, ai_model, sentence, established_ideas, iterations)  # Process sentence with AI to get the essential idea
                all_sentences.append((sentence, idea))  # Store the sentence and its idea in the list

                # Update records.csv with the new idea and chunk data
                chunk_data = "Chunk info"  # Placeholder for actual chunk data

                """THIS PART IS NOT DONE YET"""

                data.update_records_csv(idea, chunk_data, records_file)  # Update the records file with the new data

                # Add the new idea to the established ideas list if it's not already present
                if idea not in established_ideas:
                    established_ideas.append(idea)

    # Write all sentences and their ideas to sentences.csv
    data.write_sentences_to_csv(all_sentences, 'sentences.csv')

if __name__ == "__main__":
    main()  # Execute the main function when the script is run

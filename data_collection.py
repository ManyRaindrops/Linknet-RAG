# Programmed with the help of AI. This is part of stage one of the project: learning the material.

import csv
import os

def write_sentences_to_csv(sentences, output_file):
    """
    Write sentences and their associated data to a CSV file.

    :param sentences: A list of tuples where each tuple contains a sentence and its associated idea.
    :param output_file: The name of the output CSV file to write to.
    """
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Number', 'Sentence', 'Essential Idea'])  # Write the header row
        for idx, (sentence, idea) in enumerate(sentences, start=1):
            # Write each sentence with its number and associated idea
            writer.writerow([idx, sentence, idea])


def update_records_csv(idea, chunk_data, records_file):
    """
    Update records.csv with new ideas and chunk data.

    :param idea: The essential idea to be recorded.
    :param chunk_data: The chunk information associated with the idea.
    :param records_file: The name of the records CSV file to update.
    """
    records = {}

    # Read existing records if the file exists
    if os.path.exists(records_file):
        with open(records_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    # Store the idea and its associated chunk data in a dictionary
                    records[row[0]] = row[1:]  # First column is the idea, rest are chunk data

    # Update records with new idea and chunk data
    if idea not in records:
        # If the idea is new, add it with the chunk data
        records[idea] = [chunk_data]
    else:
        # If the idea already exists, add the chunk data if it's not already present
        if chunk_data not in records[idea]:
            records[idea].append(chunk_data)

    # Write updated records back to the CSV
    with open(records_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for idea, chunks in records.items():
            # Write each idea and its associated chunk data to the CSV
            writer.writerow([idea] + chunks)

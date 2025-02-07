# Programmed with the help of AI. This is part of stage one of the project: learning the material.


#import openai
#import anthropic
#import google.generativeai as google
#import ollama



"""
By default, the program uses a "thinking" approach, wherein the AI model is called to reflect on its response one time. The Ollama_API is not correct. Also, review the verification steps to that it get the system prompt, original user prompt, original model response, and the verification prompt.
"""

VERIFICATION_ITERATION_LIMIT = 2  # Maximum number of verification iterations. The maximum number of calls per sentence is thereby 3.

class ConnectProcessor:
    def __init__(self, api_service, model, sentence, existing_ideas, iterations=0):
        """
        Initialize the ConnectProcessor with the chosen API service, model, sentence, existing ideas, and verification iterations.
        This will also process the sentence immediately.

        :param api_service: The API service to use ('openai', 'anthropic', 'google_gemini', or 'ollama').
        :param model: The model to use for the chosen API service.
        :param sentence: The sentence to be processed.
        :param existing_ideas: A list of previously established essential ideas.
        :param iterations: The number of verification iterations to perform (default is 1).
        """
        self.api_service = api_service  # Store the selected API service
        self.model = model  # Store the selected model
        self.sentence = sentence  # Store the sentence to be processed
        self.existing_ideas = existing_ideas  # Store the existing ideas
        self.iterations = min(iterations, VERIFICATION_ITERATION_LIMIT)  # Limit iterations to the defined maximum

        # Immediately process the sentence upon initialization
        self.response = self.process_sentence()

    def process_sentence(self):
        """
        Process the stored sentence using the selected API service to extract essential idea information.

        :return: A string containing the essential idea information.
        """
        if self.api_service == 'openai':
            return self._process_with_openai()
        elif self.api_service == 'anthropic':
            return self._process_with_anthropic()

        #These don't work right now, but will be added later.
        #elif self.api_service == 'google_gemini':
        #    return self._process_with_google_gemini()
        #elif self.api_service == 'ollama':
        #    return self._process_with_ollama()
        #else:
        #    raise ValueError("Unsupported API service. Choose 'openai', 'anthropic', 'google_gemini', or 'ollama'.")

    def _process_with_openai(self):
        """
        Process a sentence using the OpenAI API.

        :return: A string containing the essential idea information.
        """
        try:
            # Construct a bulleted list of existing ideas for context
            ideas_context = "\n".join(f"- {idea}" for idea in self.existing_ideas)
            # Create the prompt for the OpenAI API
            prompt = (
                f"Established essential ideas:\n{ideas_context}\n\n"
                f"Based on those essential ideas, either:\n"
                f"1. State word for word the essential idea from the established list that the subject sentence represents, or\n"
                f"2. Generate a sentence that describes the essential idea represented by the subject sentence: '{self.sentence}'"
            )

            # Call the OpenAI API to get a response for the given sentence
            response = openai.ChatCompletion.create(
                model=self.model,  # Specify the model to use
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts essential ideas from sentences."},
                    {"role": "user", "content": prompt}  # Send the constructed prompt as user input
                ]
            )

            # Extract the content from the response
            idea = response['choices'][0]['message']['content'].strip()

            # Verification process
            for _ in range(self.iterations):
                # Create a verification prompt based on the initial response
                verification_prompt = (
                    f"The initial response is: '{idea}'.\n"
                    f"Please verify if this response accurately represents the essential idea from the established list. By repeating the previous response word for word, if it is good, or by changing your response as per the instructions of the first prompt."
                )

                # Call the OpenAI API again for verification
                verification_response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that extracts essential ideas from sentences."},
                        {"role": "user", "content": prompt},  # Include the original prompt for context
                        {"role": "assistant", "content": idea},  # Include the assistant's initial response
                        {"role": "user", "content": verification_prompt}  # Send the verification request
                    ]
                )

                # Extract the verification content from the response
                verification_result = verification_response['choices'][0]['message']['content'].strip()
                idea = verification_result  # Update the idea for the next iteration if needed

            return f"Idea: {idea}"  # Return the final idea after verification
        except Exception as e:
            print(f"Error processing sentence with OpenAI: {e}")  # Print error message if an exception occurs
            return "Error extracting idea"  # Return an error message

    def _process_with_anthropic(self):
        """
        Process a sentence using the Anthropic API.

        :return: A string containing the essential idea information.
        """
        try:
            # Construct a bulleted list of existing ideas for context
            ideas_context = "\n".join(f"- {idea}" for idea in self.existing_ideas)
            # Create the prompt for the Anthropic API
            prompt = (
                f"Established essential ideas:\n{ideas_context}\n\n"
                f"Based on those essential ideas, either:\n"
                f"1. State word for word the essential idea from the established list that the subject sentence represents, or\n"
                f"2. Generate a sentence that describes the essential idea represented by the subject sentence: '{self.sentence}'"
            )

            # Call the Anthropic API to get a response for the given sentence
            response = anthropic.Completion.create(
                model=self.model,  # Specify the model to use
                prompt=f"You are a helpful assistant that extracts essential ideas from sentences.\n\n{prompt}",
                max_tokens=150,  # Limit the number of tokens in the response
                stop_sequences=["\n"]  # Define stop sequences to end the response
            )

            # Extract the content from the response
            idea = response['completion'].strip()

            # Verification process
            for _ in range(self.iterations):
                # Create a verification prompt based on the initial response
                verification_prompt = (
                    f"The initial response is: '{idea}'.\n"
                    f"Please verify if this response accurately represents the essential idea from the established list. By repeating the previous response word for word, if it is good, or by changing your response as per the instructions of the first prompt."
                )

                # Call the Anthropic API again for verification, including the full context
                verification_response = anthropic.Completion.create(
                    model=self.model,
                    prompt=(
                        f"You are a helpful assistant that extracts essential ideas from sentences.\n\n"
                        f"Established essential ideas:\n{ideas_context}\n\n"
                        f"Initial prompt: {prompt}\n\n"
                        f"Initial response: '{idea}'\n"
                        f"Verification request: {verification_prompt}"
                    ),
                    max_tokens=150,  # Limit the number of tokens in the response
                    stop_sequences=["\n"]  # Define stop sequences to end the response
                )

                # Extract the verification content from the response
                verification_result = verification_response['completion'].strip()
                idea = verification_result  # Update the idea for the next iteration if needed

            return f"Idea: {idea}"  # Return the final idea after verification
        except Exception as e:
            print(f"Error processing sentence with Anthropic: {e}")  # Print error message if an exception occurs
            return "Error extracting idea"  # Return an error message

    def _process_with_google_gemini(self):
        """
        Process a sentence using the Google Gemini API.

        :return: A string containing the essential idea information.
        """
        try:
            # Construct a bulleted list of existing ideas for context
            ideas_context = "\n".join(f"- {idea}" for idea in self.existing_ideas)
            # Create the prompt for the Google Gemini API
            prompt = (
                f"Established essential ideas:\n{ideas_context}\n\n"
                f"Based on those essential ideas, either:\n"
                f"1. State word for word the essential idea from the established list that the subject sentence represents, or\n"
                f"2. Generate a sentence that describes the essential idea represented by the subject sentence: '{self.sentence}'"
            )

            # Call the Google Gemini API to get a response for the given sentence
            response = google.call(
                model=self.model,  # Specify the model to use
                prompt=(
                    f"You are a helpful assistant that extracts essential ideas from sentences.\n\n{prompt}"
                )  # Send the constructed prompt
            )

            # Extract the content from the response
            idea = response['output'].strip()  # Adjust based on actual response structure

            # Verification process
            for _ in range(self.iterations):
                # Create a verification prompt based on the initial response
                verification_prompt = (
                    f"The initial response is: '{idea}'.\n"
                    f"Please verify if this response accurately represents the essential idea from the established list. By repeating the previous response word for word, if it is good, or by changing your response as per the instructions of the first prompt."
                )

                # Call the Google Gemini API again for verification
                verification_response = google.call(
                    model=self.model,
                    prompt=(
                        f"You are a helpful assistant that extracts essential ideas from sentences.\n\n"
                        f"Initial response: '{idea}'\n"
                        f"Verification request: {verification_prompt}"
                    )  # Send the verification request
                )

                # Extract the verification content from the response
                verification_result = verification_response['output'].strip()  # Adjust based on actual response structure
                idea = verification_result  # Update the idea for the next iteration if needed

            return f"Idea: {idea}"  # Return the final idea after verification
        except Exception as e:
            print(f"Error processing sentence with Google Gemini: {e}")  # Print error message if an exception occurs
            return "Error extracting idea"  # Return an error message

    def _process_with_ollama(self):
        """
        Process a sentence using the Ollama API.

        :return: A string containing the essential idea information.
        """
        try:
            # Construct a bulleted list of existing ideas for context
            ideas_context = "\n".join(f"- {idea}" for idea in self.existing_ideas)
            # Create the prompt for the Ollama API
            prompt = (
                f"Established essential ideas:\n{ideas_context}\n\n"
                f"Based on those essential ideas, either:\n"
                f"1. State word for word the essential idea from the established list that the subject sentence represents, or\n"
                f"2. Generate a sentence that describes the essential idea represented by the subject sentence: '{self.sentence}'"
            )

            # Call the Ollama API to get a response for the given sentence
            response = ollama.call(
                model=self.model,  # Specify the model to use
                prompt=(
                    f"You are a helpful assistant that extracts essential ideas from sentences.\n\n{prompt}"
                )  # Send the constructed prompt
            )

            # Extract the content from the response
            idea = response['output'].strip()  # Adjust based on actual response structure

            # Verification process
            for _ in range(self.iterations):
                # Create a verification prompt based on the initial response
                verification_prompt = (
                    f"The initial response is: '{idea}'.\n"
                    f"Please verify if this response accurately represents the essential idea from the established list."
                )

                # Call the Ollama API again for verification
                verification_response = ollama.call(
                    model=self.model,
                    prompt=(
                        f"You are a helpful assistant that extracts essential ideas from sentences.\n\n"
                        f"Initial response: '{idea}'\n"
                        f"Verification request: {verification_prompt}"
                    )  # Send the verification request
                )

                # Extract the verification content from the response
                verification_result = verification_response['output'].strip()  # Adjust based on actual response structure
                idea = verification_result  # Update the idea for the next iteration if needed

            return f"Idea: {idea}"  # Return the final idea after verification
        except Exception as e:
            print(f"Error processing sentence with Ollama: {e}")  # Print error message if an exception occurs
            return "Error extracting idea"  # Return an error message

import os
import argparse
import PyPDF2
import openai
import logging
from joblib import load
from typing import List

# Initialize OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Load the classifier and vectorizer
classifier = load('classifier.joblib')
vectorizer = load('vectorizer.joblib')

logging.basicConfig(level=logging.INFO)

# Assuming classifier is your trained model and vectorizer is a CountVectorizer/TfidfVectorizer fitted on the training data
def classify_text(text: str) -> str:
    """
    Classifies a given text into predefined categories.
    
    Args:
    text (str): The text to classify.
    classifier: The trained text classifier.
    vectorizer: The vectorizer used to transform the text data for the model.

    Returns:
    str: The predicted label for the text.
    """
    # Transform the text data to the format used by the classifier
    text_vector = vectorizer.transform([text])

    # Predict the label of the text
    predicted_label = classifier.predict(text_vector)

    return predicted_label

def read_pdf(file_path: str) -> str:
    """Read the text content from a PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: The extracted text content.
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = " ".join([page.extract_text() for page in reader.pages])
        return text
    except Exception as e:
        logging.error(f"Failed to read PDF at {file_path}. Error: {str(e)}")

def divide_text(text: str, section_size: int) -> List[str]:
    """Divide text into sections of a specific size.

    Args:
        text (str): The text to divide.
        section_size (int): The desired section size.

    Returns:
        List[str]: The divided text sections.
    """
    return [text[i:i+section_size] for i in range(0, len(text), section_size)]

def create_anki_cards(pdf_text: str, output_file: str, model: str, temperature: float, max_tokens: int, api_key: str, section_size: int = 1000):
    """Generate Anki cards from a PDF text and save to a file.

    Args:
        pdf_text (str): The extracted PDF text.
        output_file (str): Path to save the generated flashcards.
        model (str): The OpenAI model to use for generation.
        temperature (float): The OpenAI temperature setting.
        max_tokens (int): The maximum number of tokens for the OpenAI model.
        api_key (str): The OpenAI API key.
        section_size (int, optional): The size of text sections. Defaults to 1000.
    """
    # Set the API key
    openai.api_key = api_key
    
    try:
        divided_sections = divide_text(pdf_text, section_size)
        generated_flashcards = ''
        for i, text in enumerate(divided_sections):
            # Classify the text
            predicted_label = classify_text(text)
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Create anki flashcards from {text}. The predicted label is {predicted_label}"}
            ]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            generated_flashcards += response['choices'][0]['message']['content']

            if i==0:
                break
        with open(output_file, "w") as f:
            f.write(generated_flashcards)
    except Exception as e:
        logging.error(f"Failed to create Anki cards. Error: {str(e)}")

def main_func(source_dir: str, output_dir: str, model: str, temperature: float, max_tokens: int, api_key: str):
    """Main execution function.

    Args:
        source_dir (str): Directory containing source PDFs.
        output_dir (str): Directory for output files.
        model (str): The OpenAI model to use for generation.
        temperature (float): The OpenAI temperature setting.
        max_tokens (int): The maximum number of tokens for the OpenAI model.
    """
    if not os.path.exists(source_dir):
        logging.error(f"The source directory {source_dir} does not exist.")
        return
    if not os.path.exists(output_dir):
        logging.info(f"The output directory {output_dir} does not exist. Creating it.")
        os.makedirs(output_dir)
    
    for file_name in os.listdir(source_dir):
        if file_name.endswith(".pdf"):
            pdf_text = read_pdf(os.path.join(source_dir, file_name))
            output_file = os.path.join(output_dir, file_name.rsplit(".", 1)[0] + ".txt")
            create_anki_cards(pdf_text, output_file, model, temperature, max_tokens, api_key)

def main():
    parser = argparse.ArgumentParser(description='Generate Anki flashcards from PDFs')
    parser.add_argument('--source-dir', type=str, required=True, help='Directory containing source PDFs')
    parser.add_argument('--output-dir', type=str, required=True, help='Directory for output files')
    parser.add_argument('--model', type=str, required=False, default='gpt-3.5-turbo', help='The OpenAI model to use for generation')
    parser.add_argument('--temperature', type=float, required=False, default='0.3', help='The OpenAI temperature setting')
    parser.add_argument('--max-tokens', type=int, required=False, default='2048', help='The maximum number of tokens for the OpenAI model')
    parser.add_argument('--api-key', type=str, required=False, help='The OpenAI API key')
    parser.add_argument('--section-size', type=int, default=1000, help='Section size for dividing text')
    args = parser.parse_args()
    
    api_key = args.api_key if args.api_key else os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print('No OpenAI API key found. Please set OPENAI_API_KEY in your environment or pass the --api-key argument.')
        return
    
    main_func(args.source_dir, args.output_dir, args.model, args.temperature, args.max_tokens, api_key)

if __name__ == "__main__":
    main()

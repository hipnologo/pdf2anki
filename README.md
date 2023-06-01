# pdf2anki

`pdf2anki` is a Python application that enables you to generate Anki flashcards from PDF files utilizing the power of OpenAI.

## Prerequisites

- Python 3.6 or higher
- Access to OpenAI API (ensure to set your API key as an environment variable named 'OPENAI_API_KEY')

## Installation

You can install `pdf2anki` from PyPI:

```bash
pip install pdf2anki
```

## Usage

Once installed, you can use the pdf2anki command to generate Anki cards from a directory of PDFs. The following arguments are needed:

```bash
pdf2anki --source-dir SOURCE_DIR --output-dir OUTPUT_DIR --model MODEL --temperature TEMPERATURE --max-tokens MAX_TOKENS
```

For example:

```bash
pdf2anki --source-dir ./pdfs --output-dir ./anki-cards --model gpt-3.5-turbo --temperature 0.5 --max-tokens 1000
```

## For Developers
Developers can also use pdf2anki in their Python scripts as follows:

```bash
import os
from pdf2anki.main import read_pdf, create_anki_cards

#### Define the source PDF folder and the output folder for the Anki cards
source_dir = "path/to/pdf_folder"
output_dir = "path/to/output_folder"

#### Define the parameters for the OpenAI model
model = "gpt-3.5-turbo"
temperature = 0.5
max_tokens = 1000

#### Iterate over the PDF files in the source directory
for file_name in os.listdir(source_dir):
    if file_name.endswith(".pdf"):
        # Get the full path to the source PDF
        source_pdf = os.path.join(source_dir, file_name)

        # Read the PDF text
        pdf_text = read_pdf(source_pdf)

        # Create output file path
        output_file = os.path.join(output_dir, file_name.rsplit(".", 1)[0] + ".txt")

        # Create Anki cards from the PDF text
        create_anki_cards(pdf_text, output_file, model, temperature, max_tokens)
```

## License
This project is licensed under the terms of the MIT license. For more details, see the LICENSE file.
# ML-based Quiz Generator from Java Text Files

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-blue)
![NLTK](https://img.shields.io/badge/NLTK-3.6-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0.24-blue)
![FlashText](https://img.shields.io/badge/FlashText-2.2-blue)

Are you tired of creating the same quizzes for your JAVA programming classes every semester? This project has you covered! It's an AI-powered Multiple-Choice Question (MCQ) generator that can save you time and create fresh quizzes for each session.

## Project Overview

- **Language:** Python
- **GUI Framework:** PyQt5
- **Text Processing:** NLTK, scikit-learn
- **Keyword Extraction:** FlashText
- **File Handling:** JSON, QFileDialog

## How it Works

1. **Text Processing:** We use NLTK to tokenize sentences and scikit-learn's CountVectorizer to extract relevant keywords from your JAVA lecture notes.

2. **Keyword Extraction:** Our keyword processor, powered by the FlashText library, efficiently extracts keywords from the text.

3. **MCQ Generation:** The AI generates MCQs for Java Object-Oriented Programming (OOP) by mapping keywords to sentences and replacing them with blanks. Distractors for each keyword are loaded from a JSON file.

4. **User-Friendly GUI:** We've created an intuitive user interface using PyQt5. You can select a text file, generate MCQs with a click, and download the result.

## Try It Out

1. Clone this repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Run the GUI application using `python MCQGenerator.py`.
4. Select your JAVA lecture notes, generate MCQs, and download them for your classes.
If you find it interesting, feel free to check out the code and contribute to my project 


## License

This project is licensed under the [MIT License](LICENSE).

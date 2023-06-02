import nltk
import string
import re
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
from sklearn.feature_extraction.text import CountVectorizer
import random
import json

# Function to tokenize the text into sentences
def tokenize_sentences(text):
    sentences = sent_tokenize(text)
    sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20 and len(sentence) <= 120]
    return sentences

# Function to map each keyword to the sentences in which it appears
def get_sentences_for_keyword(keywords, sentences):
    keyword_processor = KeywordProcessor()
    keyword_sentences = {}
    for word in keywords:
        lower_word = word.lower()  # Convert keyword to lowercase
        keyword_sentences[lower_word] = []
        keyword_processor.add_keyword(lower_word)
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)
        for key in keywords_found:
            keyword_sentences[key].append(sentence)
    for key in keyword_sentences.keys():
        values = keyword_sentences[key]
        values = sorted(values, key=len, reverse=True)
        keyword_sentences[key] = values
    return keyword_sentences

# Function to generate MCQs for Java OOP
def generate_java_oop_mcqs(text_file, keyword_distractor_file, num_mcqs=10, keyword_threshold=10):
    # Read the text from the file
    with open(text_file, 'r', encoding='utf-8') as file:

        full_text = file.read()

    # Tokenize the text into sentences
    sentences = tokenize_sentences(full_text)

    # Extract relevant keywords from the text
    vectorizer = CountVectorizer(lowercase=True, token_pattern=r'\b\w+\b')
    vectorizer.fit(sentences)
    keyword_counts = vectorizer.transform(sentences).sum(axis=0)
    keywords = set([keyword for keyword, count in zip(vectorizer.get_feature_names_out(), keyword_counts.tolist()[0]) if count >= keyword_threshold])

    # Load the key-distractor list from JSON file
    with open(keyword_distractor_file, 'r', encoding='utf-8') as file:

        key_distractor_list = json.load(file)

    # Map each keyword to the sentences in which it appears
    keyword_sentence_mapping = get_sentences_for_keyword(keywords, sentences)

    # Generate MCQs for the selected keywords
    mcqs = []

    for index, keyword in enumerate(keywords):
        if keyword in key_distractor_list:
            sentences_for_keyword = keyword_sentence_mapping.get(keyword, [])
            if not sentences_for_keyword or len(sentences_for_keyword) < num_mcqs:
                continue

            # Get the sentences containing the keyword
            keyword_sentences = keyword_sentence_mapping[keyword]
            num_sentences = min(num_mcqs, len(keyword_sentences))
            selected_sentences = random.sample(keyword_sentences, num_sentences)

            # Replace the keywords with blanks in the sentences
            blanked_sentences = []
            for sentence in selected_sentences:
                pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                blanked_sentence = pattern.sub("_______", sentence)
                blanked_sentences.append(blanked_sentence)

            # Combine the blanked sentences into the question
            output = ' '.join(blanked_sentences)

            # Limit the question length to one sentence or 3 lines
            output_sentences = sent_tokenize(output)
            if len(output_sentences) > 1:
                output = ' '.join(output_sentences[:3])
            else:
                output = ' '.join(output_sentences)

            # Get answer choices including the keyword and distractors
            choices = [keyword.capitalize()] + key_distractor_list[keyword]

            # Randomly shuffle the answer choices
            random.shuffle(choices)

            # Remove special characters from the question and choices
            output = remove_special_characters(output)
            choices = [remove_special_characters(choice) for choice in choices]

            # Prepare the MCQ question structure
            quiz_question = {
                'question': output,
                'choices': choices,
            }

            # Find the correct option
            correct_option = chr(ord('A') + choices.index(keyword.capitalize()))

            # Append the MCQ question to the list
            mcqs.append({
                'question': output,
                'choices': choices,
                'correct_option': correct_option
            })

    return mcqs

# Function to remove special characters from a string
def remove_special_characters(text):
    special_chars = ['•', '❑','']  # Add more special characters if needed
    for char in special_chars:
        text = text.replace(char, '')
    return text

# Example usage
java_oop_mcqs = generate_java_oop_mcqs('mcq.txt', 'list.json', num_mcqs=random.randint(10, 15), keyword_threshold=10)

# enable the following snippet to Print the generated MCQs on command line

# for idx, mcq in enumerate(java_oop_mcqs):
#     print(f"MCQ {idx+1}:")
#     print("Question:", mcq['question'])
#     print("Choices:")
#     for i, choice in enumerate(mcq['choices']):
#         print(f"{chr(ord('A') + i)}) {choice}")
#     print("Correct Option:", mcq['correct_option'])
#     # print()

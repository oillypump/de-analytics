paragraphs = [
    "This is a sample paragraph. It contains several sentences. Each sentence has some words in it.",
    "Another paragraph with some different words in it. This paragraph is shorter."
]

# Define the words to count
words_to_count = ['sample', 'sentences']

# Create an empty dictionary to store the word counts
word_counts = {}

# Iterate over each paragraph
for paragraph in paragraphs:
    # Convert the paragraph to lowercase and split it into words
    words = paragraph.lower().split()
    print(words)
    # Iterate over each word in the list of words
    for word in words:
        # If the word is in the list of words to count, increment its count
        if word in words_to_count:
            # If the word is already in the dictionary, increment its count
            if word in word_counts:
                word_counts[word] += 1
            # If the word is not yet in the dictionary, add it with a count of 1
            else:
                word_counts[word] = 1

# Print the count of each word
for word in words_to_count:
    if word in word_counts:
        print(f"{word}: {word_counts[word]}")
    else:
        print(f"{word}: 0")

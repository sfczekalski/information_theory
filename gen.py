from collections import Counter, defaultdict
from numpy.random import choice


def read_file(file_name):
    file = open(file_name, 'r')
    return file.read()


def avg_word_length(text):
    words = text.split()

    return sum([len(word) for word in words]) / len(words)


def get_alphabet():
    """Generate a list of all possible characters in the alphabet, plus digits."""
    alphabet = [' '] + [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('0'), ord('9') + 1)]
    return alphabet


def generate_random(length):
    """Generate random text, in which all characters have an equal chance of appearing."""
    alphabet = get_alphabet()
    random_text = ''.join([alphabet[choice(len(alphabet))] for _ in range(length)])
    return random_text


def alphabet_with_probabilities(sort=False):
    """Calculate the probability of each letter in a corpus.
        :param sort : whenever to sort letters according to their probability
        :returns probabilities : dictionary of (letter, probability)
    """

    file_name = 'data/wiki.txt'
    text = read_file(file_name=file_name)

    letter_counter = Counter(text)
    counter_sum = sum(letter_counter.values())
    probabilities = {k: v / counter_sum for k, v in letter_counter.items()}

    if sort:
        probabilities = {k: v for k, v in sorted(probabilities.items(), key=lambda item: item[1], reverse=True)}

    return probabilities


def generate_random_with_p(length):
    """Generate random text, in which all characters have an equal chance of appearing."""

    alphabet, probabilities = zip(*alphabet_with_probabilities().items())
    text = ''.join([choice(a=alphabet, p=probabilities) for _ in range(length)])
    return text


def bigrams():
    """Generate bigrams starting with two most common letters in corpus."""

    alphabet = alphabet_with_probabilities(sort=True)

    # find top letters, excluding the space
    top_letters = [k for k, v in alphabet.items() if k != ' '][:2]

    file_name = 'data/wiki.txt'
    text = read_file(file_name=file_name)
    bigrams_dict = {key: defaultdict(int) for key in top_letters}
    top_letters_counters = {k: 0 for k in top_letters}
    for i in range(1, len(text)):

        # ignore spaces
        if text[i] == ' ':
            continue

        if text[i - 1] in top_letters:

            bigrams_dict[text[i - 1]][text[i]] += 1
            top_letters_counters[text[i - 1]] += 1

    for l in top_letters:
        bigrams_dict[l] = {k: v / top_letters_counters[l] for k, v in sorted(bigrams_dict[l].items(),
                                                                             key=lambda item: item[1], reverse=True)}

    return bigrams_dict


bigrams_dict = bigrams()
print(bigrams_dict['e'])
print(bigrams_dict['a'])

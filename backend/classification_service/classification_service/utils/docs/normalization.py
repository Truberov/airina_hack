# from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from razdel import tokenize

# stop_words = set(stopwords.words('russian'))

legal_stop_words = {
    'дом', 'корпус', 'строение', 'квартира', 'офис', 'банк',
    'счет', 'бик', 'инн', 'кпп', 'номер', 'дата', 'год', 'месяц', 'день',
    'рубль', 'копейка', 'тысяча', 'миллион', 'процент', 'штука', 'кг', 'ндс', 'i', 'ii', 'iii', 'n', 'г'
}

morph = MorphAnalyzer()

def normalize_text(text):
    # Токенизация текста
    tokens = [token.text.lower() for token in tokenize(text)]

    # Удаление стоп-слов, знаков препинания
    # filtered_tokens = [token for token in tokens if token.isalpha() and token not in stop_words]

    # Лемматизация токенов
    lemmatized_tokens = [morph.parse(token)[0].normal_form for token in tokens]

    # Удаление юридических стоп-слов
    filtered_lemmatized_tokens = [token for token in lemmatized_tokens if token not in legal_stop_words]

    # Объединение токенов обратно в текст
    normalized_text = ' '.join(filtered_lemmatized_tokens)

    return normalized_text
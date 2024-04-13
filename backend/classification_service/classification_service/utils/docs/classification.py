import os

import torch
from transformers import BertTokenizer, BertModel
import torch.nn as nn


class DocumentClassifier(nn.Module):
    def __init__(self, num_classes):
        super(DocumentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-multilingual-cased')
        self.dropout = nn.Dropout(0.3)
        self.fc = nn.Linear(self.bert.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        _, pooled_output = self.bert(input_ids=input_ids, attention_mask=attention_mask, return_dict=False)
        dropout_output = self.dropout(pooled_output)
        logits = self.fc(dropout_output)
        return logits


MODEL_PATH = './model_data/trained_model3.pth'
TOKENIZER = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

def get_doc_class(text, model_path=MODEL_PATH):
    classes = {
        'Договоры': 10,
        'Заявления': 7,
        'Приказы': 4,
        'Соглашения': 6,
        'Устав': 0,
        'Доверенность': 8,
        'Акт': 1,
        'Решение': 9,
        'Оферта': 5,
        'Счет': 3,
        'bill': 2
    }

    # Создание словаря для сопоставления меток классов с индексами
    label_to_index = {label: index for label, index in classes.items()}
    # Загрузка обученной модели
    num_classes = len(label_to_index)
    model = DocumentClassifier(num_classes)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    # Инициализация токенизатора
    tokenizer = TOKENIZER

    # Перенос модели на устройство (CPU или GPU)
    device = torch.device('cpu')
    model.to(device)

    # Создание обратного словаря для сопоставления индексов с метками классов
    index_to_label = {index: label for label, index in label_to_index.items()}
    # text = normalize_text(text)

    # Токенизация и подготовка входных данных
    encoding = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=512,
        return_token_type_ids=False,
        padding='max_length',
        return_attention_mask=True,
        return_tensors='pt',
        truncation=True
    )
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    # Получение предсказаний модели
    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        _, predicted_class_index = torch.max(outputs, 1)

    # Преобразование индекса предсказанного класса в метку класса
    predicted_class = index_to_label[predicted_class_index.item()]

    return predicted_class

import torch
from transformers import BertTokenizer, BertModel
import torch.nn as nn

from .normalization import normalize_text

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

async def get_doc_class(text, model_path=MODEL_PATH):
    classes = {
        'contract': 10,
        'application': 7,
        'order': 4,
        'arrangement': 6,
        'statute': 0,
        'proxy': 8,
        'act': 1,
        'determination': 9,
        'contract offer': 5,
        'invoice': 3,
        'bill': 2
    }

    label_to_index = {label: index for label, index in classes.items()}
    num_classes = len(label_to_index)
    model = DocumentClassifier(num_classes)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    tokenizer = TOKENIZER

    device = torch.device('cpu')
    model.to(device)

    index_to_label = {index: label for label, index in label_to_index.items()}
    text = normalize_text(text)

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

    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        _, predicted_class_index = torch.max(outputs, 1)

    predicted_class = index_to_label[predicted_class_index.item()]

    return predicted_class

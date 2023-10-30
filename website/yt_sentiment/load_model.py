from transformers import AutoTokenizer, TFAutoModelForSequenceClassification


def load_model(path):
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = TFAutoModelForSequenceClassification.from_pretrained(path)

    return model, tokenizer

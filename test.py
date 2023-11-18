from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

if __name__ == "__main__":
    msg = "curso de cocina 10€"

    pipe = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7")

    # model = AutoModelForSequenceClassification.from_pretrained("./iamodels/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
    # tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
    # pipe = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)
    cosa = pipe(msg,
                candidate_labels=["venta", "gasto"],
                )
    print(cosa)
    cosa = pipe(msg,
                candidate_labels=["alimentación/básicos", "carburantes", "formación", "inversión",
                                  "subscripciones",
                                  "seguros", "autopista", "ocio", "nomina", "bares", "restaurantes"],
                )
    print(cosa)
    """
    qa_model = pipeline("question-answering", model="MMG/bert-base-spanish-wwm-cased-finetuned-sqac")
    question = "¿Qué dia fue ayer?"
    context = "Ayer hice una compra. Hoy es día 18 de noviembre de 2023"
    cosa = qa_model(question=question, context=context, inputs="")
    print(cosa)
    """

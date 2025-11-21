from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

model_name = "bert-base-uncased"
num_labels = 2
batch_size = 8
epochs = 2
lr = 5e-5

dataset = load_dataset("imdb")
train_dataset = dataset["train"].shuffle(seed=42).select(range(1000))  # small subset for demo
eval_dataset = dataset["test"].shuffle(seed=42).select(range(200))

tokenizer = AutoTokenizer.from_pretrained(model_name)

def preprocess(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=128)

train_dataset = train_dataset.map(preprocess, batched=True)
eval_dataset = eval_dataset.map(preprocess, batched=True)

train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
eval_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=epochs,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    learning_rate=lr,
    evaluation_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
    save_strategy="no"  # don't save checkpoints for this demo
)

trainer = Trainer(
    model=model,
    trainig_args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

# ---- Train ----
trainer.train()

# ---- Evaluate ----
results = trainer.evaluate()
print(results)
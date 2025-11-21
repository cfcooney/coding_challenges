import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
from datasets import load_dataset
# STEP1: imports


# STEP2: define variables
epochs = 2
batch_size = 2
learning_rate = 1e-5
model_name = "bert-base-uncased"
num_labels = 2
device = "cuda" if torch.cuda.is_available() else "cpu"

# STEP 3: load the data
data = load_dataset("imdb")
train_set = data["train"]["texts"][:1000]
train_labels = data["train"]["labels"][:1000]

#STEP 4: load tokenizer and model with encoding
tokenizer = AutoTokenizer.from_pretrained(model_name)
encoding = tokenizer(train_set, truncation=True, padding=True, return_tensors="pt")

model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.to(device)

# STEP 5: Create a simple torch dataset

class DataClass(torch.utils.data.Dataset):
    def __init__(self, encoding, labels):
        self.encodings = encoding
        self.labels = labels

    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        item = {key: value[idx] for key, value in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

train_dataset = DataClass(encoding, train_labels)
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# STEP 6 Define optimizer and model for train
optimizer = AdamW(model.parameters(), lr=learning_rate)

model.train()

# STEP 7 Define a training loop
for epoch in range(epochs):
    for batch in train_dataloader:
        batch = {key: value.to(device) for key, value in batch.items()}

        outputs = model(**batch)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"  Loss: {loss.item():.4f}")







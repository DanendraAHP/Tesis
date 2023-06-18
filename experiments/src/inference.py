from transformers import (
    T5ForConditionalGeneration,
    DataCollatorForSeq2Seq,
)
import torch
from tqdm import tqdm

class ModelInference:
    def __init__(self, batch_size, dataset, model, tokenizer, inference_len) -> None:
        self.batch_size = batch_size
        self.model = model
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)
        self.datacollator = DataCollatorForSeq2Seq(tokenizer, model=model)
        self.dataset = dataset
        self.tokenizer = tokenizer
        self.inference_len = inference_len
    def inference(self):
        inference_dataset = [self.dataset[i] for i in range(len(self.dataset['input_ids']))]
        inference_dataset = self.datacollator(inference_dataset)
        pred_text = []
        for i in tqdm(range(0, len(inference_dataset['input_ids']), self.batch_size)):
            generated_text = self.model.generate(inference_dataset['input_ids'][i:i+self.batch_size].to(self.device), max_length=self.inference_len)
            decoded_text = self.tokenizer.batch_decode(generated_text, skip_special_tokens=True)
            pred_text+=decoded_text
        return pred_text
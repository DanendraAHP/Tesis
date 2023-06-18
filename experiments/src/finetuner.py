from transformers import (
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
)
import torch

class FineTuner:
    def __init__(self, model, save_path, tokenizer, train_dataset, eval_dataset) -> None:
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = model.to(self.device)
        self.save_path = save_path
        self.tokenizer = tokenizer
        self.train_dataset = train_dataset
        self.eval_dataset = eval_dataset
        print(self.device)
    def fine_tune(self, arg):
        data_collator = DataCollatorForSeq2Seq(self.tokenizer, model=self.model)
        trainer = Seq2SeqTrainer(
            self.model,
            arg,
            train_dataset=self.train_dataset,
            eval_dataset=self.eval_dataset,
            data_collator=data_collator,
            tokenizer=self.tokenizer,
        )
        trainer.train()
        self.model.save_pretrained(self.save_path)
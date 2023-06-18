import re
from src.utils import extract_quadruplet, extract_triplet
from tqdm.auto import tqdm

class Evaluator:
    def __init__(self, task_type, postprocessor):
        # == Metrics ==
        self.precision_fn = lambda n_tp, n_pred: float(n_tp) / float(n_pred) if n_pred != 0 else 0
        self.recall_fn = lambda n_tp, n_gold: float(n_tp) / float(n_gold) if n_gold != 0 else 0
        self.f1_fn = (
            lambda precision, recall: (2 * precision * recall) / (precision + recall)
            if precision != 0 or recall != 0
            else 0
        )
        self.task_type = task_type
        self.postprocessor = postprocessor
    def score(self, pred, gold):
        assert len(pred) == len(gold)
        n_tp, n_gold, n_pred = 0, 0, 0

        for i in range(len(pred)):
            n_gold += len(gold[i])
            n_pred += len(pred[i])

            for t in pred[i]:
                if t in gold[i]:
                    n_tp += 1
                
        precision = self.precision_fn(n_tp, n_pred)
        recall = self.recall_fn(n_tp, n_gold)
        f1 = self.f1_fn(precision, recall)
        return {"precision": precision, "recall": recall, "f1": f1}
    
    # == Evaluation ==
    def evaluate(self, pred_seqs, gold_seqs):
        assert len(pred_seqs) == len(gold_seqs)
        num_samples = len(gold_seqs)

        all_labels, all_preds = [], []

        for i in tqdm(range(num_samples)):
            if self.task_type=='quadruplet':
                #gold_list = extract_quadruplet(gold_seqs[i], original_sentences[i], self.postprocessor)
                #pred_list = extract_quadruplet(pred_seqs[i], original_sentences[i], self.postprocessor)
                gold_list = extract_quadruplet(gold_seqs[i])
                pred_list = extract_quadruplet(pred_seqs[i])
            elif self.task_type=='triplet':
                #gold_list = extract_triplet(pred_seqs[i], original_sentences[i], self.postprocessor)
                #pred_list = extract_triplet(pred_seqs[i], original_sentences[i], self.postprocessor)
                gold_list = extract_triplet(gold_seqs[i])
                pred_list = extract_triplet(pred_seqs[i])
            all_labels.append(gold_list)
            all_preds.append(pred_list)

        raw_scores = self.score(all_preds, all_labels)
        return raw_scores, all_labels, all_preds
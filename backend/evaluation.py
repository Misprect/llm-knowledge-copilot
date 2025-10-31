##Explanation
#BLEU (from NLTK) → measures how similar your generated text is to the reference (based on matching words or short word sequences).
#ROUGE (from rouge_score) → measures recall — how much of the reference content your prediction successfully covers.
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

def evaluate_metrics(prediction: str, reference: str):
    try:
        # BLEU (sentence-level)
        ##Explanation
        #BLEU normally compares n-gram overlaps (1-gram, 2-gram, 3-gram, etc.) between prediction and reference.
        #But if your prediction is short or doesn’t have higher-order overlaps, BLEU can return zero, even for decent text.
        #So we use a smoothing function to avoid zeros for smaller overlaps.
        #SmoothingFunction()
        #It’s part of NLTK. It smooths out harsh penalties when your prediction doesn’t have enough long word overlaps.
        chencherry = SmoothingFunction()
        bleu = sentence_bleu([reference.split()], prediction.split(), smoothing_function=chencherry.method1)

        # ROUGE
        ##Explanation
        #ROUGE-1: compares overlapping unigrams (words) between prediction & reference.
        #ROUGE-L: compares longest common subsequence (LCS) — measures how much of the reference’s structure is preserved.
        scorer = rouge_scorer.RougeScorer(["rouge1", "rougeL"], use_stemmer=True)
        rouge = scorer.score(reference, prediction)

        # Basic length-based metrics (word counts)
        #It checks how close your model’s answer length is to the expected answer length.
        ref_len = len(reference.split())
        pred_len = len(prediction.split())
        mse = mean_squared_error([ref_len], [pred_len])
        mae = mean_absolute_error([ref_len], [pred_len])
        rmse = np.sqrt(mse)

        #The .fmeasure part comes from ROUGE — it combines precision (correct words found) and recall (how many reference words covered).
        return {
            "bleu": round(float(bleu), 4),
            "rouge1_f": round(rouge["rouge1"].fmeasure, 4),
            "rougeL_f": round(rouge["rougeL"].fmeasure, 4),
            "mse_length": round(float(mse), 4),
            "mae_length": round(float(mae), 4),
            "rmse_length": round(float(rmse), 4),
        }
    except Exception as e:
        return {"error": str(e)}

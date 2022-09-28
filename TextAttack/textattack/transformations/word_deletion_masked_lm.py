import re

import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

from textattack.shared import utils

from .word_deletion import WordDeletion


class WordDeletionMaskedLM(WordDeletion):
    def __init__(
        self,
        masked_language_model="bert-base-uncased",
        tokenizer=None,
        max_length=512,
        window_size=float("inf"),
        max_candidates=50,
        min_confidence=5e-4,
        batch_size=16,
    ):
        super().__init__()
        self.max_length = max_length
        self.window_size = window_size
        self.max_candidates = max_candidates
        self.min_confidence = min_confidence
        self.batch_size = batch_size

        if isinstance(masked_language_model, str):
            self._language_model = AutoModelForMaskedLM.from_pretrained(
                masked_language_model
            )
            self._lm_tokenizer = AutoTokenizer.from_pretrained(
                masked_language_model, use_fast=True
            )
        else:
            self._language_model = masked_language_model
            if tokenizer is None:
                raise ValueError(
                    "`tokenizer` argument must be provided when passing an actual model as `masked_language_model`."
                )
            self._lm_tokenizer = tokenizer
        self._language_model.to(utils.device)
        self._language_model.eval()
        self.masked_lm_name = self._language_model.__class__.__name__

    def _encode_text(self, text):
        encoding = self._lm_tokenizer(
            text,
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )
        return {k: v.to(utils.device) for k, v in encoding.items()}

    def _get_transformations(self, current_text, indices_to_modify):
        transformed_texts = []
        if len(current_text.words) > 1:
            for i in indices_to_modify:
                transformed_texts.append(current_text.delete_word_at_index(i))
        return transformed_texts

    def extra_repr_keys(self):
        return ["masked_lm_name", "max_length", "max_candidates", "min_confidence"]

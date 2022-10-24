from textattack.augmentation import DeletionAugmenter

text = "I have enjoyed watching that movie, it was amazing."

deletion_aug = DeletionAugmenter()
deletion_aug.augment(text)

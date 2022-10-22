from textattack.augmentation import CLAREAugmenter
clareAugmenter = CLAREAugmenter()
s = "What I cannot create, I do not understand."
print(clareAugmenter.augment(s))


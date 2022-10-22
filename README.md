# SeniorProject_NLPAttack

## 1. Augment - Word deletion
### Method 1 : Command line
* **`cd Textattack`**
* **_`./textattack_run augment --recipe clare --pct-words-to-swap .1 --transformations-per-example 5 --exclude-original --input-csv ./inputs/my_input.csv --output-csv ./inputs/outputs/word_delete_output.csv --overwrite --input-column /text/`_**
  
  + **[`-recipe`]** : use recipy clare
  + **[`--pct-words-to-swap`]** : word swap percentage (delete percentage) is 0.1
  + **[`--transformations-per-example 5`]** :  make 5 examples per 1 sentence  with transformation (WordDeletion)
  + **[`--input-csv ./inputs/my_input.csv`]** : read inputs/my_input.csv
  + **[`--output-csv ./inputs/outputs/word_delete_output.csv`]** : It makes result file in inputs/outputs, and file name is 'word_delete_output.csv'
  + **[`--overwrite`]** : if result file already exists, overwrite augmentation result  


#### Method 1 - Result

* Input file : `inputs/my_input.csv`  
  <img width="294" alt="image" src="https://user-images.githubusercontent.com/30529101/196148729-25adb424-33c0-4e85-99f3-fe2d54cab41b.png">  
* Output file : `inputs/outputs/word_delete_output.csv`  
  <img width="278" alt="image" src="https://user-images.githubusercontent.com/30529101/196148928-4f7bbc16-1036-4c91-b4c0-fed5c2399fe6.png">  

### Method 2 : Import Augmenter
* python3 my_augementation.py  
  + import clare augmenter and input example

#### Method 2 - Result
* `vim my_augmentation.py`  
  <img width="452" alt="image" src="https://user-images.githubusercontent.com/30529101/196147507-2a574588-b879-454c-9cf9-d19b20275d7f.png">  
* `python3 my_augmentation.py`  
  <img width="469" alt="image" src="https://user-images.githubusercontent.com/30529101/196148343-efaaef4f-f6e6-45c0-be13-bfbe43dc494d.png">  



## TextAttack End-to-End : with Word Deletion
### Training : First, train model
* Select the Rotten Tomatoes Movie Review dataset using `peek-dataset`
  + **`./textattack_run peek-dataset --dataset-from-huggingface rotten_tomatoes`**
    <img width="1386" alt="image" src="https://user-images.githubusercontent.com/30529101/196360233-11f9c85f-759e-42c3-8f59-5c20185e8d47.png">  
    
* Train a Model
  + **_`./textattack_run train --model-name-or-path distilbert-base-uncased --dataset rotten_tomatoes --model-num-labels 2 --model-max-length 64 --per-device-train-batch-size 128 --num-epochs 3`_** 
  
    + **[`--model distilbert-base-uncased`]** : Using distilbert, uncased version, from `transformers`
    + **[`--dataset rotten_tomatoes`]** : On the Rotten Tomatoes dataset
    + **[`--model-num-labels 2`]** : has 2 labels
    + **[`--model-max-length 64`]** : With a maximum sequence length of 64
    + **[` --per-device-train-batch-size 128`]** : Batch size of 128
    + **[`--num-epochs 3`]** : 3 epochs
    
    <img width="1379" alt="image" src="https://user-images.githubusercontent.com/30529101/196363624-a704005c-6cea-4adf-bb14-2cbf307c2635.png">

    
### Evaluation
* evaluate it using `textattack eval`
* `textattack eval` will automatically load the evaluation data from training
  + **_`./textattack_run eval --num-examples 1000 --model ./outputs/2022-10-18-15-51-52-377473/best_model/ --dataset-from-huggingface rotten_tomatoes --dataset-split test`_**  
  
    + **[`--model ./outputs/2022-10-18-15-51-52-377473/best_model/`]** : Trained model (In previous `train` step)
    <img width="572" alt="image" src="https://user-images.githubusercontent.com/30529101/196363911-b5860d21-3f8c-4c9a-9ad3-057c922b1b1d.png">


### Attack
* Attack our pre-trained model
* Use **`clare`** attack recipe

  + **_`./textattack_run attack --recipe clare --num-examples 100 --model ./outputs/2022-10-18-15-51-52-377473/best_model/ --dataset-from-huggingface rotten_tomatoes --dataset-split test`_**
    <img width="385" alt="image" src="https://user-images.githubusercontent.com/30529101/196367182-e1597941-cdf9-4a57-8115-42c1262fa0f1.png">
    + Our model was 83% successful, and attack 83 examples (since the attack won't run if an example is originally mispredicted)
    + Attack success rate is 98.8% that means **clare** failed to find an adversarial example only 1.2% of the time
    
    
----


    


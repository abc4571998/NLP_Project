# SeniorProject_NLPAttack

## 1. Augment - Word deletion
### Method 1 : Command line
* Delete word randomly
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


## 2. Augment - Word deletion with Grammar checking
* The previous 'word_deletion' method randomly deletes a word.
* Deleting important words, such as subjects or verbs, results in incorrect grammar of the sentence.
* So I added the grammar check function to the word_deletion as a grammar check.
* Gramformer resolves errors by changing the word sequence or inserting words, but has problems performing word_deletion.
* If the verb is deleted and a grammatical error occurs, the gramformer inserts the verb. It looks like word_insertion.
* I wanted to delete grammatically, so I added a function to make good sentences without deleting the subject and verb.
  <img width="731" alt="image" src="https://user-images.githubusercontent.com/30529101/197599028-5b195e79-d5c9-4255-af0b-0713b959b126.png">
  <img width="644" alt="image" src="https://user-images.githubusercontent.com/30529101/197599177-7cad64bf-1e27-4d6e-b8b7-00de6e3d8344.png">


## TextAttack End-to-End : with Word Deletion
### Training : First, train model
* Select the Rotten Tomatoes Movie Review dataset using `peek-dataset`
  + **`./textattack_run peek-dataset --dataset-from-huggingface rotten_tomatoes`**
    <img width="1386" alt="image" src="https://user-images.githubusercontent.com/30529101/196360233-11f9c85f-759e-42c3-8f59-5c20185e8d47.png">  
    
* Train a Model
  + **_`./textattack_run train --model-name-or-path distilbert-base-uncased --dataset rotten_tomatoes --model-num-labels 2 --model-max-length 64 --per-device-train-batch-size 128 --num-epochs 3`_** 
  
    + **[`--model distilbert-base-uncased`]** : Using distilbert, uncased version, from `transformers`
    + **[`--dataset rotten_tomatoes`]** : On the Rotten Tomatoes dataset
    + **[`--model-num-labels 2`]** : has 2 labels (0 or 1)
    + **[`--model-max-length 64`]** : With a maximum sequence length of 64 (The longest input is 51 words, so we can cap our maximum sequence length (--model-max-length) at 64)
    + **[` --per-device-train-batch-size 128`]** : Batch size of 128
    + **[`--num-epochs 3`]** : 3 epochs
    
    <img width="1379" alt="image" src="https://user-images.githubusercontent.com/30529101/196363624-a704005c-6cea-4adf-bb14-2cbf307c2635.png">

  + **_`./textattack_run train --model-name-or-path distilbert-base-uncased --dataset rotten_tomatoes --model-num-labels 2 --model-max-length 64 --per-device-train-batch-size 128 --num-epochs 5`_**
    + + **[`--num-epochs 5`]** : 5 epochs
      <img width="739" alt="image" src="https://user-images.githubusercontent.com/30529101/197519659-92860878-2c9c-460c-8249-4107e647b3c8.png">
      <img width="855" alt="image" src="https://user-images.githubusercontent.com/30529101/197520165-f001c204-4cde-46da-8b2f-588252ba7734.png">

    
### Evaluation
* evaluate it using `textattack eval`
* `textattack eval` will automatically load the evaluation data from training
  + **_`./textattack_run eval --num-examples 1000 --model ./outputs/2022-10-18-15-51-52-377473/best_model/ --dataset-from-huggingface rotten_tomatoes --dataset-split test`_**  
  
    + **[`--model ./outputs/2022-10-18-15-51-52-377473/best_model/`]** : Trained model (In previous `train` step)
    <img width="572" alt="image" src="https://user-images.githubusercontent.com/30529101/196363911-b5860d21-3f8c-4c9a-9ad3-057c922b1b1d.png">

  
  + **_`./textattack_run eval --num-examples 1000 --model ./outputs/2022-10-24-20-52-58-294706/best_model/ --dataset-from-huggingface rotten_tomatoes --dataset-split test`_**  
    <img width="601" alt="image" src="https://user-images.githubusercontent.com/30529101/197520923-90749f0a-33f6-4e51-9b99-f434d3832f35.png">


### Attack
* Attack our pre-trained model
* Use **`clare`** attack recipe

  + **_`./textattack_run attack --recipe clare --num-examples 100 --model ./outputs/2022-10-18-15-51-52-377473/best_model/ --dataset-from-huggingface rotten_tomatoes --dataset-split test`_**
    <img width="385" alt="image" src="https://user-images.githubusercontent.com/30529101/196367182-e1597941-cdf9-4a57-8115-42c1262fa0f1.png">
    + Our model was 83% successful, and attack 83 examples (since the attack won't run if an example is originally mispredicted)
    + Attack success rate is 98.8% that means **clare** failed to find an adversarial example only 1.2% of the time
    
  + **_`./textattack_run attack --recipe clare --num-examples 100 --model ./outputs/2022-10-24-20-52-58-294706/best_model/ --dataset-from-huggingface rotten_tomatoes --dataset-split test`_**
    <img width="380" alt="image" src="https://user-images.githubusercontent.com/30529101/197522184-d63a4886-e909-4cb2-a860-07ef9eb4d639.png">


  + **_`./textattack_run attack --recipe clare --num-examples 100 --model ./outputs/2022-10-24-20-52-58-294706/best_model/ --dataset-from-huggingface rotten_tomatoes --dataset-split test`_**
    <img width="378" alt="image" src="https://user-images.githubusercontent.com/30529101/197606094-6b6f4976-e628-4ca5-b1e2-d1034873f882.png">
    <img width="392" alt="image" src="https://user-images.githubusercontent.com/30529101/197609622-e5667ef6-fbdf-4a3b-8891-ee6022469397.png">


    <img width="392" alt="image" src="https://user-images.githubusercontent.com/30529101/197652843-97cda2f9-4752-49f1-bcc8-294eb128f3ff.png">

    <img width="388" alt="image" src="https://user-images.githubusercontent.com/30529101/197665638-fb5d77da-ed35-4f5f-8c4b-52182019ab3e.png">


----


    


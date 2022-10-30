#### Table of contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Using on Dev environment (Python)](#python)
4. [Using on Browser](#browser)


# Vietnamese Question Generation <a name="introduction"></a>
This project publishes a method of using syntax and shallow semantic for Vietnamese question generation from text.


Analyzing the structure of a sentence, also known as parsing a sentence, is the core technique of syntax-based Question Generation (QG).


In this proposal, I has been using VnCoreNLP, which is a fast and accurate NLP annotation pipeline for Vietnamese, providing rich linguistic annotations through key NLP components of word segmentation, POS tagging, named entity recognition (NER) and dependency parsing.
## Installation <a name="installation"></a>
- `Python 3.6+` if using [a Python wrapper of VnCoreNLP](https://github.com/thelinhbkhn2014/VnCoreNLP_Wrapper). To install this wrapper, users have to run the following command:

    `$ pip install py_vncorenlp` 
    
- `Java 1.8+` 
- File  `VnCoreNLP-1.1.1.jar` (27MB) and folder `models` (115MB) are placed in the same working folder. In the `./Code` folder run file `init_vncorenlp.py` to download the VnCoreNLP model:

    `$ python init_vncorenlp.py` 
    
- To use QG from the API, users have to install the `Flask` framework and flask-cors package which is Flask's built-in CORS module for by passing the cross-origin resource policy while requesting from the API endpoint:

    `$ pip install Flask, flask-cors` 
    
## Using on Dev environment (Python) <a name="python"></a>
Run the following command to use VnCoreNLP as an API:

    $ vncorenlp -Xmx2g <FULL-PATH-to-VnCoreNLP-jar-file> -p <Port-number> -a "wseg,pos,ner,parse" 
    
 \<FULL-PATH-to-VnCoreNLP-jar-file\> is the full path to ./Code/vncorenlp/VnCoreNLP-1.1.1.jar (/Users/khanhnguyen/Document/QG/Code/vncorenlp/VnCoreNLP-1.1.1.jar)

The default value of \<Port-number\> is 9000.

```
from vncorenlp import VnCoreNLP
from utils import *

# Load patterns
# Change this pattern_path to your own full path to 
pattern_path = '../pattern/pattern.txt'
with open(pattern_path, "r") as f:
    patterns = f.read().split('\n')

# Connect to the VnCoreNLP API
annotator = VnCoreNLP(address="http://127.0.0.1", port=9000)

text = "Khanh là sinh viên."

# To perform word segmentation, POS tagging, NER and then dependency parsing
annotated_text = annotator.annotate(text)
annotated_text = annotated_text['sentences']
tmp = {}
for i, at in enumerate(annotated_text):
    tmp[i] = at
annotated_text = tmp
print(question_generation(annotated_text, patterns))
```
The output is list of json, each json represents for one sentence and its automatically generated question and answer pairs.
```
[{'sentence': 'Khanh là sinh viên .', 'qas': [{'question': 'Khanh là ai ?', 'answer': 'sinh viên', 'pattern_id': 0}, {'question': 'Ai là sinh viên ?', 'answer': 'Khanh', 'pattern_id': 1}]}]
```
## Using on Browser <a name="browser"></a>
Run the following command to use VnCoreNLP as an API:

    $ vncorenlp -Xmx2g <FULL-PATH-to-VnCoreNLP-jar-file> -p <Port-number> -a "wseg,pos,ner,parse" 
    
Then run the file `api_qg.py` in the folder `./Code` to use Question Generation as an API:

    $ python api_qg.py
Open file `./Code/index.html` by your browser and generate questions from text input.

![](https://github.com/khanhduynguyen170900/vqg/blob/main/Gif_Demo_QG.gif)

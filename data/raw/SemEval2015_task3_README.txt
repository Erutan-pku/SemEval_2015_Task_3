TEST dataset for SemEval-2015 Task #3: Answer Selection in Community Question Answering


SUMMARY

English:
test_task3_English.xml -- test input for subtasks A and B, English

TASK B:
test_task3_Arabic.xml -- test input for subtask A, Arabic (there is no subtask B for Arabic)

The gold annotations are in the _gold directory; they are in the same format as for the development dataset.


IMPORTANT

To use this test dataset, the participants should download (1), and most likely also (2) and (3):

1. the training dataset
2. the dev dataset
3. the official scorer (participants would only be able to use it on the dev data)
4. the format checker

They can all be found here: http://alt.qcri.org/semeval2015/task3/index.php?id=data-and-tools


INPUT DATA FORMAT

The input data format, together with some statistics is described here:

http://alt.qcri.org/semeval2015/task3/index.php?id=detailed-task-and-data-description

The TEST input data is in the same format as the DEV input data.


EXPECTED OUTPUT FORMAT

See the README of the format checker and of the scorer.


SCORING

See the README of the scorer.


DATASET USE

The development dataset is intended to be used as a development-time evaluation dataset as the participants develop their systems. However, the participants are free to use the dataset in any way they like, e.g., they can add it to their training dataset as well.


LICENSE

Licensing: 
- the scripts and all files released for the task are free for general research use 
- you should use the following citation in your publications whenever using these resources:

@InProceedings{nakov-EtAl:2015:SemEval,
  author    = {Nakov, Preslav  and  M\`{a}rquez, Llu\'{i}s  and  Magdy, Walid  and  Moschitti, Alessandro  and  Glass, Jim  and  Randeree, Bilal},
  title     = {{SemEval}-2015 Task 3: Answer Selection in Community Question Answering},
  booktitle = {Proceedings of the 9th International Workshop on Semantic Evaluation},
  series    = {SemEval '15},
  month     = {June},
  year      = {2015},
  address   = {Denver, Colorado},
  publisher = {Association for Computational Linguistics},
  pages     = {269--281},
  url       = {http://www.aclweb.org/anthology/S15-2047}
}


CREDITS

Task Organizers:

    Lluís Màrquez
        Arabic Language Technologies (ALT)
        Qatar Computing Research Institute (QCRI), Qatar
    James Glass (CSAIL, MIT)
    Walid Magdy (ALT-QCRI, Qatar)
    Alessandro Moschitti (ALT-QCRI, Qatar)    
    Preslav Nakov (ALT-QCRI, Qatar)
    Bilal Randeree (Qatar Living, Qatar)

Task website: http://alt.qcri.org/semeval2015/task3/

Contact: semeval-cqa@googlegroups.com

Acknowledgements: This research is part of the Interactive sYstems for Answer Search (Iyas) project, conducted by the Arabic Language Technologies (ALT) group at the Qatar Computing Research Institute (QCRI), HBKU within the Qatar Foundation. 

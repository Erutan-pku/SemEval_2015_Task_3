==============================================================
CQA-QL English corpus for SemEval-2015 Task 3
"Answer Selection in Community Question Answering"
Version 2.0: September 15, 2014
==============================================================

This file contains the basic information regarding the CQA-QL English corpus provided for the SemEval-2015 task "Answer Selection in Community Question Answering". The current version (2.0, September 15, 2014) corresponds to the release of the training data sets. Test sets will be provided in future versions. All changes and updates on these data sets are reported in Section 1 of this document.

[1] LIST OF VERSIONS

  v2.0 [2014/09/15]: initial distribution of the TRAINING data sets. 
      The following changes are observed from distribution 1.0:
    - Training and development sets have been provided
    - Several cosmetic changes apply to the XML labels 
    - The "ANNOTATION" field was renamed to "GOLD"
    - The set of labels for the "ANNOTATION" field have been slightly simplified
    - The Yes/No type of questions are now labeled also at the question level: see new "QGOLD_YN" attribute 
    - Please, disregard the formatting of the TRIAL dataset and stick to the current version 2.0

  v1.0 [2014/06/30]: initial distribution of the TRIAL data sets


[2] CONTENTS OF THE DISTRIBUTION 2.0

We are providing the following files:

* README.txt 
  this file

* datasets/CQA-QL-train.xml
  traning data set; 2,600 questions
  
* datasets/CQA-QL-devel.xml
  development data set; 300 questions

* datasets/CQA-QL-devel-input.xml
  the development data set, but with the gold labels hidden -- to be used as input at development time

* datasets/CQA-QL-devel-gold.txt
  the gold labels for subtask A -- to be used as GOLD at development time

* datasets/CQA-QL-devel-gold-yn.txt
  the gold labels for subtask B -- to be used as GOLD-YN at development time

* datasets/generate-devel-gold.pl
  PERL script that generates the last three files above from datasets/CQA-QL-devel.xml

Note: The training and the development sets are obtained by randomly splitting the questions 
into two sets of ~90% and ~10% of the total size.

* datasets/CQA-QL-trial.txt
  trial data set, as distributed on 2014/06/30; included just for completeness with respect to the previous distribution

This distribution is directly downloadable from the official SemEval-2015 Task 3 website http://alt.qcri.org/semeval2015/task3/index.php?id=data-and-tools

Licensing: 
- these datasets are free for general research use 
- you should use the following citation in your publications whenever using this resource:

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



[3] DATA FORMAT

The datasets are XML-formated and the text encoding is UTF-8.

A dataset file is a sequence of examples (Questions):

<root>
  <Question> ... <\Question>
  <Question> ... <\Question>
  ...
  <Question> ... <\Question>
</root>

Each Question tag has a list of attributes, as in the following example:

<Question QID="Q1" QCATEGORY="Pets and Animals" QDATE="2009-03-07 19:24:00" QUSERID="U1" QTYPE="YES_NO" QGOLD_YN="Yes">

- QID: internal question identifier
- QCATEGORY: the question category, according to the Qatar Living taxonomy  
- QDATE: date of posting
- QUSERID: internal identifier for the user who posted the question; consistent across questions
- QTYPE: type of question, can be "GENERAL" or "YES_NO" 
- QGOLD_YN: overall Yes/No summary of the set of good answers for the concrete YES_NO question (or "Not Applicable" in the case of "GENERAL" questions); this value is a class label to be predicted at test time

The structure of a Question is the following:

<Question ...>
  <QSubject> text </QSubject>
  <QBody> text </QBody>
    <Comment> ... </Comment>
    <Comment> ... </Comment>
    ...
    <Comment> ... </Comment>
</Question>

The text between the <QSubject> and the </QSubject> tags is the short version of the question as provided by user QUSERID.
The text between tags <QBody> and </QBody> is the long version of the question as provided by user QUSERID.
What follows is a list of Comments, each corresponding to an answer (to the focus question) posted by a particular user.

Every Comment tag has some attributes, as in the following example:

<Comment CID="Q1_C1" CUSERID="U4" CGOLD="Good" CGOLD_YN="No">

 - CID: Internal identifier of the comment: the part before the "_" encodes the question number
 - CUSERID: Internal identifier of the user posting the comment
 - CGOLD: human assessment about whether the comment is "Good", "Bad", "Potential" or "Dialogue". This is a class label to be predicted at test time.
 - CGOLD_YN: human assessment on whether the comment is answering positively ("Yes"), negatively ("No") or as unsure ("Unsure") to the question (or "Not Applicable" in the case of "GENERAL" questions); this label is only available at training time; at test time, participating systems are not required to produce CGOLD_YN but only QGOLD_YN.

Comments are structured as follows:

<Comment ...>
  <CSubject> text </CSubject>
  <CBody> text </CBody>
</Comment>

The text between the <CSubject> and the </CSubject> tags is the short version of the comment.
The text between the <CBody> and the </QBody> tags is the long version of the comment.


[4] MORE INFORMATION ON THE CQA-QL CORPUS

The source of the CQA-QL corpus is the Qatar Living Forum data (http://www.qatarliving.com). A sample of questions and comments threads was automatically selected and posteriorly manually filtered and annotated with the categories defined in the task.

The manual annotation was a joint effort between the CSAIL-MIT and ALT-QCRI groups (see organizers below). 

After a first internal labeling of the TRIAL dataset (50+50 questions) by several independent annotators, we defined the annotation procedure and prepared detailed annotation guidelines. 

Amazon's Mechanical Turk was used to collect the human annotations for the large corpus. Nicole Schmidt (CSAIL-MIT) implemented the Mechanical Turk-based annotation. Several HITs were defined to produce all the required annotation: HIT 1) Select appropriate example questions and classify them as GENERAL vs. YES_NO; HIT 2) Annotate every comment in the general questions as "Good", "Bad", "Potential" or "Dialogue" tags. 3) Annotate the "YES_NO" questions with the same information at the comment level, plus a label ("Yes"/"No"/"Unsure") indicating whether the comment answers the question with a clear "Yes", a clear "No" or in an undefined way. In all HITs, we collected the annotation of several annotators for each decision (there were between 3 and 5 human annotators) and resolved discrepancies using majority voting. Ties lead to the elimination of some comments and even of complete examples. 
The "Yes"/"No"/"Unsure" labels at the question level (QGOLD_YN) were assigned automatically based on the "Yes"/"No"/"Unsure" labels at the comment level. More concretely, a YES_NO question is labeled as "Unsure" except in the case in which there is a majority of "Yes" or "No" labels among the "Yes"/"No"/"Unsure" labels from the comments that are labeled as "Good". In that case, the majority label is assigned.


Some statistics about the datasets (training & development):

TRAIN:
- QUESTIONS:
    - TOTAL:        2600
    - GENERAL:      2376 (91.38%)
    - YES_NO :       224 ( 8.62%)
- COMMENTS:
    - TOTAL:       16541
    - MIN:             1
    - MAX:           143
    - AVG:             6.36
- CGOLD VALUES:
	Good:       8069 (48.78%)
	Bad:        2981 (18.02%)
	Potential:  1659 (10.03%)
	Dialogue:   3755 (22.70%)
	Not English:  74 ( 0.45%)
	Other:         3 ( 0.02%)
- CGOLD_YN COMMENT VALUES (excluding "Not Applicable"):
	yes:         346 (43.52%)
	no:          236 (29.69%)
	unsure:      213 (26.79%)
- QGOLD_YN VALUES (excluding "Not Applicable"):
	yes:          87 (38.84%)
	no:           47 (20.98%)
	unsure:       90 (40.18%)


DEVEL:
- QUESTIONS:
    - TOTAL:         300
    - GENERAL:       266 (88.67%)
    - YES_NO :        34 (11.33%)
- COMMENTS:
    - TOTAL:        1645
    - MIN:             1
    - MAX:            32
    - AVG:             5.48
- CGOLD VALUES:
	Good:        875 (53.19%)
	Bad:         269 (16.35%)
	Potential:   187 (11.37%)
	Dialogue:    312 (18.97%)
	Not English:   2 ( 0.12%)
	Other:         0 ( 0.00%)
- CGOLD_YN COMMENT VALUES (excluding "Not Applicable"):
	yes:          62 (53.91%)
	no:           32 (27.83%)
	unsure:       21 (18.26%)
- QGOLD_YN VALUES (excluding "Not Applicable"):
	yes:          16 (47.06%)
	no:            8 (23.53%)
	unsure:       10 (29.41%)


[5] CREDITS

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

Acknowledgements: This research is part of the Interactive sYstems for Answer Search (Iyas) project, conducted by the Arabic Language Technologies (ALT) group at the atar Computing Research Institute (QCRI) within the Qatar Foundation. 

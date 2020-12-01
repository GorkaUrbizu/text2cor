# LEA Coreference Scorer

Implementation of the **LEA** coreference evaluation metric integrated into the CoNLL official scorer v8.01.

## Description

LEA is a Link-Based Entity-Aware metric that is designed to overcome the shortcomings of the previous evaluation metrics.
LEA evaluates a set of entities as follows:

<img src="http://www.sciweavers.org/tex2img.php?eq=%5Cfrac%7B%5Csum_%7Be_i%5Cin%20E%7D%20%28%5Ctext%7Bimportance%7D%28e_i%29%20%5Ctimes%20%5Ctext%7Bresolution-score%7D%28e_i%29%29%7D%7B%5Csum_%7Be_k%5Cin%20E%7D%20importance%28e_k%29%7D&bc=White&fc=Black&im=jpg&fs=12&ff=modern&edit=0" align="center" border="0" alt="\frac{\sum_{e_i\in E} (\text{importance}(e_i) \times \text{resolution-score}(e_i))}{\sum_{e_k\in E} importance(e_k)}" width="321" height="46" />

For each entity, **LEA** considers how important the entity is and how well it is resolved.
In the provided implementation, we consider the size of an entity as a measure of importance, i.e. 
the more prominent entities of the text get higher importance values. 
However, according to the end-task or domain used, one can choose other importance measures based on other factors like the entity type or the included mention types.

The number of unique links in an entity with "n" mentions is:

<img src="http://www.sciweavers.org/tex2img.php?eq=link%28e%29%3Dn%20%5Ctimes%20%28n-1%29%2F2&bc=White&fc=Black&im=jpg&fs=12&ff=modern&edit=0" align="center" border="0" alt="link(e)=n \times (n-1)/2" width="172" height="19" />

The resolution score of an entity is computed as the fraction of its correctly resolved coreference links.
Assume "e" is an input entity and "R" is the set of all output entities. The resolution score of "e" is computed as:

<img src="http://www.sciweavers.org/tex2img.php?eq=%5Ctext%7Bresolution-score%7D%28e%29%3D%5Csum_%7Br_j%20%5Cin%20R%7D%5Cfrac%7Blink%28e%20%5Ccap%20r_j%29%7D%7Blink%28e%29%7D&bc=White&fc=Black&im=jpg&fs=12&ff=modern&edit=0" align="center" border="0" alt="\text{resolution-score}(e)=\sum_{r_j \in R}\frac{link(e \cap r_j)}{link(e)}" width="268" height="49" />

Assume "K" is the set of key entities and "R" is the set of response entities. Having the definitions of "importance" and "resolution-score", **LEA** recall is computed as:

<img src="http://www.sciweavers.org/tex2img.php?eq=%5Ctext%7BRecall%7D%3D%5Cfrac%7B%5Csum_%7Bk_i%20%5Cin%20K%7D%20%28%7Ck_i%7C%20%5Ctimes%20%5Csum_%7Br_j%20%5Cin%20R%7D%5Cfrac%7Blink%28k_i%20%5Ccap%20r_j%29%7D%7Blink%28k_i%29%7D%29%7D%7B%5Csum_%7Bk_p%20%5Cin%20K%7D%7Ck_p%7C%7D&bc=White&fc=Black&im=jpg&fs=12&ff=modern&edit=0" align="center" border="0" alt="\text{Recall}=\frac{\sum_{k_i \in K} (|k_i| \times \sum_{r_j \in R}\frac{link(k_i \cap r_j)}{link(k_i)})}{\sum_{k_p \in K}|k_p|}" width="285" height="53" />

Precision is computed by changing the role of the key and response entities.

## Usage

**LEA** is integrated into the official CoNLL scorer v8.01 available at http://conll.github.io/reference-coreference-scorers.  
The usage of the official CoNLL scorer (Pradhan et al., 2014) is as follows:


     perl scorer.pl <metric> <key> <response> [<document-id>]


     <metric>: the metric desired to score the results. one of the following values:

     muc: MUCScorer (Vilain et al, 1995)
     bcub: B-Cubed (Bagga and Baldwin, 1998)
     ceafm: CEAF (Luo et al., 2005) using mention-based similarity
     ceafe: CEAF (Luo et al., 2005) using entity-based similarity
     blanc: BLANC (Luo et al., 2014) BLANC metric for gold and predicted mentions
     lea: LEA (Moosavi and Strube, 2016)
     all: uses all the metrics to score

     <key>: file with expected coreference chains in CoNLL-2011/2012 format

     <response>: file with output of coreference system (CoNLL-2011/2012 format)
 
     <document-id>: optional. The name of the document to score. If name is not
                    given, all the documents in the dataset will be scored. If given
                    name is "none" then all the documents are scored but only total
                    results are shown.

##References

    Nafise Sadat Moosavi and Michael Strube. 2016. 
    Which Coreference Evaluation Metric Do You Trust? A Proposal for a Link-based Entity Aware Metric. 
    In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics.

    Sameer Pradhan, Xiaoqiang Luo, Marta Recasens, Eduard Hovy, Vincent Ng, and Michael Strube. 2014. 
    Scoring coreference partitions of predicted mentions: A reference implementation. 
    In Proceedings of the 52nd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers),
    Baltimore, Md., 22–27 June 2014, pages 30–35.


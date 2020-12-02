# Text2Cor: Sequence to Sequence Coreference Resolution

### By: Gorka Urbizu Garmendia

Sequence to Sequence Coreference Resolution for English, using a Transformer.

datasets not provided here, you can find them at:

- [ARRAU dataset](https://catalog.ldc.upenn.edu/LDC2013T22)

- [PreCo dataset](https://preschool-lab.github.io/PreCo/)

[more coreference resources](https://github.com/gorka96/Coreference-Corpora-Resources)  (+20 languages, add yours!)



# PREPROCESSING

###  mmax to conll

ARRAU:
python3 mmax2conll.py

(fout = train dev test)

PreCo:
already at conll format

### conll 2 src/trg:

Train: all #1199779 seq
4+ sen, 100+ words, 1/4 of them (unlest shortest or full doc)

python3 word2seq.py data/train_ARRAU_sen.conll data/train_ARRAU_seq

python3 word2seqPreco.py data/preco.conll data/train_preco_seq

Test/dev:

python3 word2doc.py data/dev_ARRAU.conll data/dev_ARRAU
python3 word2doc.py data/test_ARRAU.conll data/test_ARRAU

# BPE

## train BPE

subword-nmt learn-bpe -s 16000 < BPE/en_raw.txt > BPE/en16k.bpe

result:
'''
Spea@@ ker . 1 . Okay . U@@ m the s the scene opens up with um you see a tree . k K@@ ay . And there 's a ladder coming out o of the tree . and there 's a man at the top of the ladder . you can n't see him yet . And then it shifts . and you see him . pl@@ uc@@ king a p@@ ear from the tree . And you watch him pl@@ uck a few pears . and he 'd drop them into thing . but I do n't he 's wearing like an ap@@ ron with huge pockets . But I do n't think you see the ap@@ ron at first . I do n't know if that 's important or not . And uh and then he gets down out of the tree . and he dum@@ ps ail pears into the basket and the basket 's full . and one of the pears drops down to the floor . and he picks it up . and he takes ker@@ chief off . and he wi@@ pes it off . and places it in in the basket which is very full . That 's why it fell off in the first place . And um then he clim@@ bs back up the ladder . and he and he starts picking pears again . And then while he 's up in the ladder . let 's see is it while he 's up in the ladder . Or or before . U@@ m anyway . a guy comes by leading a goat . And the goat 's a@@ a@@ ar@@ r@@ r but and they do n't talk to each other . they do n't I do n't think they even look at each other . and the guy walks by . And you watch the goat . disappearing all the way . and then then you 're back to the man in the tree . And he 's up there in the tree . And then definitely when he 's up there . a kid comes by on a bicycle . From the direction where the goat man left . okay . And U@@ m the bicycle 's way too big for the kid . I 'm giving you all these details .
'''

# BPE src

subword-nmt apply-bpe -c BPE/en16k.bpe < data/test_ARRAU.src > data/test_ARRAU_bpe.src
subword-nmt apply-bpe -c BPE/en16k.bpe < data/dev_ARRAU.src > data/dev_ARRAU_bpe.src
subword-nmt apply-bpe -c BPE/en16k.bpe < data/train_ARRAU_seq.src > data/train_ARRAU_seq_bpe.src
subword-nmt apply-bpe -c BPE/en16k.bpe < data/train_ARRAU_seq2.src > data/train_ARRAU_seq2_bpe.src

./BPE/subword-nmt/apply_bpe.py -c BPE/en16k.bpe < data/train_ARRAU_seq.src > data/train_ARRAU_seq_bpe.src
./BPE/subword-nmt/apply_bpe.py -c BPE/en16k.bpe < data/preco_seq.src > data/preco_seq_bpe.src

cat data/train_ARRAU_seq_bpe.src data/preco_seq_bpe.src > data/train_all_seq_bpe.src
cat data/train_ARRAU_seq.trg data/preco_seq.trg > data/train_all_seq_bpe.

#TRG split:

sed 's/|/ | /g' data/train_ARRAU.trg > data/train_ARRAU_split.trg

# FAIRSEQ

fairseq-preprocess --source-lang src --target-lang trg --trainpref data/train_all_seq_bpe --validpref data/dev_ARRAU_bpe --testpref data/test_ARRAU_bpe --destdir data-bin/text2cor_all_seq_bpe.bin --workers 8

## Train the transformer model

fairseq-train data-bin/text2cor_all_seq_bpe.bin --arch transformer_iwslt_de_en --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.1 --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 --dropout 0.3 --weight-decay 0.0001 --criterion label_smoothed_cross_entropy --label-smoothing 0.1 --no-epoch-checkpoints --num-workers 8 --max-epoch 10 --save-dir checkpoints/transformer_text2cor_all_seq_bpe --skip-invalid-size-inputs-valid-test --max-tokens 4096 --update-freq 8

## inference 

fairseq-generate data-bin/text2cor_all_seq_bpe.bin --path checkpoints/transformer_text2cor_all_seq_bpe/checkpoint_best.pt --beam 5 --skip-invalid-size-inputs-valid-test > outputs/output.txt

grep ^S outputs/output.txt | cut -f2- | sed -r 's/(@@ )|(@@ ?$)//g' > outputs/sequences.txt
grep ^T outputs/output.txt | cut -f2- > outputs/target.txt
grep ^H outputs/output.txt | cut -f3- > outputs/hypotheses.txt

## scorer

./scorer/scorer.pl all outputs/test.gold outputs/test.pred


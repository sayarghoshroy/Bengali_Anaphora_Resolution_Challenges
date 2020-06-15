# Bengali Anaphora Resolution Challenges

### Outline of a Rule Based Anaphora Resolution System for Bengali

<p align="justify">
We present an anaphora resolution system for Bengali which utilizes linguistic features for disambiguation of possible antecedents of a particular anaphor. The system accepts a sentence in UTF8 Bengali script as its input, identifies the pronominal anaphors and detects all possible antecedents for that particular anaphor. Using a set of hierarchical rules, the system disambiguates and selects the best contextual antecedent from the set of possibilities. The system is evaluated on a manually tagged dataset.
</p>

<p align="justify">
This study shows exactly how far a system with linguistic rules can go and illustrates the stepping off point after which the use of core knowledge becomes paramount. However, for a simple rule based system, it performs reasonably well often disambiguating a set of possible antecedents down to the most obvious and correct choice.
</p>

### Disambiguation Features
1. <p align="justify">Part-Of-Speech information: The POS tag not only identifies pronouns and nouns, but also helps us recognize named entities in text.</p>
2. <p align="justify">Number: The pronoun and its antecedent must have number-agreement i.e references to singular and plural entities must tally with the antecedents themselves.</p></p>
3. <p align="justify">Person: Agreement of person helps classify one particular antecedent as more probable than another given other features are equivalent.</p>
4. <p align="justify">Status: Honorifics used give us clues as to which particular person the referent is actually referring to.</p>
5. <p align="justify">Morphological : Morphological features are used to identify number in nouns and type of referent in case of pronouns.</p>

#### For details, refer to the [full report](https://github.com/sayarghoshroy/Bengali_Anaphora_Resolution_Challenges/blob/master/report.pdf).

---

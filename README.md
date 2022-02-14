# INCEpTION postprocessor

This is a project-specific script to postprocess texts that were annotated in the semantic annotation software [INCEpTION](https://inception-project.github.io).

## About the project
This project was developed at the German Seminar at the University of Zurich (chair Merten, Digitalisierte Kommunikationsräume).

We annotated German social media texts with two custom tagsets: 
- A **formal** tagset (e.g. 'NP' for nominal phrases, 'In' for interjection etc.)
- A **functional** tagset (e.g. 'DaÄ' for expressions of thanks, 'DaO' for the object of the expression of thanks, 'EvB_l' for lexical parts of an evaluation etc.)

The text that was to be annotated contained one comment per line, e.g.: 
```sh
@t_jo_maria danke! Super, dass du deinen Weg gefunden hast 😊
So stolz uf dich ❤️
```


We exported the annotated texts in the format 'WebAnno TSV v3.3 (WebAnno v3.x)'. The INCEpTION output looks like this: 

```sh
#Text=@t_jo_maria danke! Super, dass du deinen Weg gefunden hast 😊
15-1	1294-1295	@	_	Ad\_@[184]	
15-2	1295-1305	t_jo_maria	_	Ad\_@[184]	
15-3	1306-1311	danke	_	CR[185]|DaÄ[186]	
15-4	1311-1312	!	_	CR[185]|DaÄ[186]	
15-5	1313-1318	Super	AdjP\_subj[7]	CR[185]|EvÄ\_p[187]|EvB\_l[188]	
15-6	1318-1319	,	AdjP\_subj[7]	CR[185]|EvÄ\_p[187]	
15-7	1320-1324	dass	AdjP\_subj[7]	CR[185]|EvÄ\_p[187]|EvO[189]	
15-8	1325-1327	du	AdjP\_subj[7]	CR[185]|EvÄ\_p[187]|EvO[189]	
15-9	1328-1334	deinen	AdjP\_subj[7]	CR[185]|EvÄ\_p[187]|EvO[189]	
15-10	1335-1338	Weg	AdjP\_subj[7]	CR[185]|EvÄ\_p[187]|EvO[189]	
15-11	1339-1347	gefunden	AdjP\_subj[7]	CR[185]|EvÄ\_p[187]|EvO[189]	
15-12	1348-1352	hast	AdjP\_subj[7]	CR[185]|EvÄ\_p[187]|EvO[189]	
15-13	1353-1355	😊	AdjP\_subj[7]	CR[185]|EvÄ\_p[187]|EM\_freu[190]	

#Text=So stolz uf dich ❤️
16-1	1356-1358	So	AdjP[8]	SUP\_Zu[191]	
16-2	1359-1364	stolz	AdjP[8]	SUP\_Zu[191]	
16-3	1365-1367	uf	AdjP[8]	SUP\_Zu[191]	
16-4	1368-1372	dich	AdjP[8]	SUP\_Zu[191]	
16-5	1373-1375	❤️	AdjP[8]	SUP\_Zu[191]|EM\_bez[192]	

```

In the INCEpTION output, different lines/comments are seperated by empty lines. For comment, the entire comment is outputted, followed by the tokenized line with all tags a token was tagged with. The lines with tokens are tab-seperated with the token in third position, the formal tag(s) in fourth position and functional tags in fifth position. If a tag was tagged with multiple tags from one tagset, those tags are seperated by a verticular bar '|'. 

This script postprocesses the INCEpTION output so that phrases or comments that were tagged with a specific tag are outputted. 
Each command searches through all txt-files in the 'data' folder and returns either the entire comment a tag occurs in or just the 'phrases' within the comment that were tagged with the specific tag. 

## How to use the script

Examples:

- Write all comments with noun phrases to the output file: 

```sh
 $ python3 inception_postprocess.py --input data/ --output belegliste_NP.txt --formal NP

```
- Write all comments with expressions of thanks to the output file: 

```sh
 $ python3 inception_postprocess.py --input data/ --output belegliste_DaAe.txt --functional DaÄ

```
- Write all comments that contain tokens which are both an interjection and an evaluation to the output file:

```sh
 $ python3 inception_postprocess.py --input data/ --output belegliste_NP_DaAe.txt --tag1 NP --tag2 DaÄ

```
- Write all noun phrases (not the entire comment!) to the output file:  

```sh
$ python3 inception_postprocess.py --input data/ --output belegliste_p_NP.txt --phrase NP

```






## Folder Structure
```
project
│   README.md
│   inception_postprocess.py    
│
└───data
│       text1.txt
│       text2.txt
|       text3.txt
│  
└───beleglisten_comments
│       belegliste_c_NP.txt
│       belegliste_c_DaÄ.txt
|       belegliste_c_NP_DaÄ.txt
│  
└───beleglisten_phrases
        belegliste_p_NP.txt

```


## Requirements
- Python version 3.6 or newer



## License
This script is licensed under the term of the MIT License, see the file LICENSE for more details. 
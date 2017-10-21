##Introduction
---------
This is just a personal using python oop practice. This is a tool for getting ebridge score data for XJTLU students, and for fun :) **If you want to play with it, `cd` to this directory and use your console `pip install requirements.txt` to install all relied packages.**

The program has three main classes:
1. The first one is `Ebridge()`, which is used to post personal data to direct to score page to get score data. The property `score_data` is very useful for I have been structed all score items as followed: 
```python
[{'Attempt': '1',
  'credit': '5',
  'detail_assessment': [{'assessment_type': 'Coursework',
                         'component_title': 'Writing Tasks',
                         'mark': '82',
                         'weight': '30'},
                        {'assessment_type': 'Examination',
                         'component_title': 'Writing',
                         'mark': '95',
                         'weight': '20'},
                        {'assessment_type': 'Examination',
                         'component_title': 'Listening',
                         'mark': '69',
                         'weight': '25'},
                        {'assessment_type': 'Coursework',
                         'component_title': 'Speaking',
                         'mark': '75',
                         'weight': '25'}],
  'grades': 'P',
  'mark': '80',
  'module_code': 'SPA001',
  'module_title': 'Spanish Stage 1',
  'period': 'SEM2'}
  ]
  ```
  This is similar with your ebridge one module score:
  ![image](http://ww3.sinaimg.cn/large/0060lm7Tly1fko0vy0flrj31kw0enacu.jpg)

2. The second class is 
> self.score_list. #This is most useful, the data structure just like this:

  
> self.name, your name

> self.ID, your ID card nubmer 

> self.average(), return your average.


---------
More method will be extended...

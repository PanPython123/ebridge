##Introduction
---------

This is just a personal using python oop practice. This is a tool for getting ebridge score data for XJTLU students, and for fun :) **If you want to play with it, `cd` to this directory and use your console `pip install requirements.txt` to install all relied packages.**


##Funny Classes
---------

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

2. The second class is `Score(Ebridge)`, it extends class `Ebridge()` mainly using `scroe_data` from father class, it has three useful methods ¡`analyze()`, if you failed some courses, it will display your unpassed information like this: 
```python
Dear Somebody, These modules you did really terrible: 
ModuleCode              Description                                                     YourScore
+-----------------------+----------------------------------------------------------------+----------+
SomeMoudle              SomeD                                                             Score under 40
SomeMoudle              SomeD                                                             Score under 40
+-----------------------+----------------------------------------------------------------+----------+
```

Besides, if you want to see detail, it will ask for your detial score if yur input `Y`. The method has been concealed in the as the inner method for `Score` class. You can also unwrapped with it to have a fun. The detail score is like this:
```python
Dear Somebody, These modules you did really terrible: 
ModuleCode              Assessments/Coursework       Type                YourScore
+-----------------------+----------------------------+-----------------+----------+
SomeModule               Some Type                    Some CW         under 40
+-----------------------+----------------------------------------------+----------+
SomeModule               Some Type                    Some CW         under 40
+-----------------------+----------------------------------------------+----------+
SomeModule               Some Type                    Some CW         under 40
+-----------------------+----------------------------------------------+----------+
SomeModule               Some Type                    Some CW         under 40
+-----------------------+----------------------------------------------+----------+
```

Lastly, the public method `average` would print your average score driectly. 

3. The third class `FakeScore(Ebridge)`, extends from Ebridge, has a parallel relationship with class `Score()`, which means these two classes do not have interact. This part is most wonderful, for it could produce fake score `HTML!` for you. the gif if followed:

![fake_score](http://ww3.sinaimg.cn/large/0060lm7Tly1fkqabf09j3g30qo0f04qs.gif)


The file tree is `ebridge_website` and `web_frame`. `ebridge_website` is performed as the temeplate to render `fake_score.html` and `web_frame` is for inserting data. IF you call `fake_score()` method in the `FakeScore()` class, you will get a file name `fake_score.html` in the `ebridge_website`, the effect is just like in the gif :) 


##Other properties
------------------

Some other properties are waiting for you to have a try:

> self.name, your name

> self.ID, your ID card nubmer

---------
Maybe this project would be invalid once if ebridge changes the score data

This is just a personal using python oop practice. This is a tool for getting ebridge score data for XJTLU students.

If you run this program directly, you could view your average score if you input the right account and password!
Some useful instance and method are following:
> self.score_list. #This is most useful, the data structure just like this:
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
  This is similar as your ebridge one module score:
  ![image](http://ww3.sinaimg.cn/large/0060lm7Tly1fko0vy0flrj31kw0enacu.jpg)
  
> self.name, your name

> self.ID, your ID card nubmer 

> self.average(), return your average.


---------
More method will be extended...

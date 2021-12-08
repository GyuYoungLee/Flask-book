* (Book) 플라스트 웹 프로그래밍 (윤정현, 2021)
* (Book) 점프 투 플라스크 (박응용, 2020)
* (Book) 깔끔한 파이썬, 탄탄한 백엔드 (송은우, 2019)



### flask shell

q = Question(subject='pybo', content='hello', create_date=datetime.now())  
db.session.add(q)  
db.session.commit()  

q = Question(subject='flask', content='good', create_date=datetime.now())  
db.session.add(q)  
db.session.commit()  

Question.query.all()  
Question.query.filter(Question.id==1).all()  
Question.query.filter(Question.subject.like('%flask%')).all()  

q = Question.query.get(2)  
q.subject = 'bad'  
db.session.commit()  

q = Question.query.get(1)  
db.session.delete(q)  
db.session.commit()  

q = Question.query.get(2)  
a = Answer(question=q, content='yes', create_date=datetime.now())    
db.session.add(a)  
db.session.commit()  

a.quesion  
q.answer_set

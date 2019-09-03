# -*- encoding=UTF-8 -*-

from instagram import app, db
from flask_script import Manager
from instagram.models import User, Image, Comment
from sqlalchemy import or_, and_
import random
manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('User'+str(i),'a'+str(i+1)))
        for j in range(0, 3):
            db.session.add(Image(get_image_url(),i+1))
            for k in range(0, 3):
                db.session.add(Comment('This is a comment' + str(k), 1+3*i+j, i+1))
    db.session.commit()
# 数据库更新
    for i in range(50, 100, 2):
        user = User.query.get(i)
        user.username = '[New1]' + user.username
    User.query.filter_by(id=51).update({'username': '[New2]'})
    db.session.commit()
# 数据库删除 查出对象删除
    for i in range(50, 100, 2):
        comment = Comment.query.get(i+1)
        db.session.delete(comment)
    db.session.commit()
# 数据库的查询
    print(1, User.query.all())
    print(2, User.query.get(3))
    print(3, User.query.filter_by(id=5).first())
    print(4, User.query.order_by(User.id.desc()).offset(1).limit(2).all())
    print(5, User.query.filter(User.username.endswith('0')).limit(3).all())
    print(6, User.query.filter(or_(User.id == 88, User.id == 99)).all())
    print(7, User.query.filter(and_(User.id > 88, User.id < 93)).all())
# 分页
    print(8, User.query.paginate(page=1, per_page=10).items)
# 排序分页
    print(9, User.query.order_by(User.id.desc()).paginate(page=1, per_page=10).items)
# 通过用户查images
    user = User.query.get(1)
    print(10, user.images)
# 通过image知道它的用户是谁
# 在class这个类里面没有user这个属性
# 通过backref在User类中指定images 的backref是User
    image = Image.query.get(1)
    print(11, image, image.user)


if __name__ == '__main__':
    manager.run()


#!/usr/bin/env python
#coding:utf-8

import os
from app import create_app,db
from app.models import User,Role,Post
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand

COV=None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV=coverage.coverage(branch=True,include='app/*')
    COV.start()

#FLASKY_CONFIG是环境变量,根据环境变量的获取不同的配置,
#默认是获取开发配置
app=create_app(os.getenv('FLASK_CONFIG') or 'default')

manager=Manager(app)
"""
创建manage对象,该对象以flask的程序app为参数创建,后续进行
app的管理,使启动服务器时支持命令行.
Example:
    开启服务器:python manage.py runserver
"""

migrate=Migrate(app,db)
"""
创建migrate对象,用来管理数据库的迁移等相关工作,Migrate接受两个参数
一个是flask的程序对象app,一个是SQLAlchemy数据库管理对象
"""

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Post=Post)

manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    """运行单元测试"""
    import unittest
    tests=unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
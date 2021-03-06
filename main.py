from flask import Flask
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from gevent.libev.corecext import os

from views import index_blu,passport_blu,user_blu,news_blu,admin_blu
from models import db
from utils.common import show_top_6_news_style,show_news_status_name,show_news_status_style_name,show_top_7_news_style,set_after_request_handle_fuc

# 创建flask应用对象
app = Flask(__name__)

# 加载配置
app.config.from_pyfile("config.ini")

# 创建蓝图，且注册到app
app.register_blueprint(index_blu)
app.register_blueprint(passport_blu)
app.register_blueprint(user_blu)
app.register_blueprint(news_blu)
app.register_blueprint(admin_blu)

basedir = os.path.abspath(os.path.dirname(__file__))


# 初始化数据库
db.init_app(app)
# 添加过滤器
app.add_template_filter(show_top_6_news_style)
app.add_template_filter(show_news_status_name)
app.add_template_filter(show_news_status_style_name)
app.add_template_filter(show_top_7_news_style)

# 设置钩子函数，可以在调用视图函数之前自动执行
set_after_request_handle_fuc(app)
# 添加数据库迁移等工具
manager = Manager(app)
# 生成migrate对象，用来数据库迁移
migrate = Migrate(app,db)
# 添加db命令
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    # app.run()
    manager.run()
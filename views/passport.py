from flask import request

from models import db
from models.index import User

from . import passport_blu

@passport_blu.route("/passport/register", methods=["GET", "POST"])
def register():
    # 1. 提取数据
    mobile = request.json.get("mobile")
    password = request.json.get("password")
    image_code = request.json.get("image_code")
    smscode = request.json.get("smscode")
    # 2. 测试数据
    print(mobile, password, image_code, smscode)

    # 创建一个新用户
    # 查询是否有这个相同的用户
    if db.session.query(User).filter().first():
        return "已经注册过了"
    # 注册用户为未注册用户
    # 将新用户的数据插入到数据库
    user = User()
    user.nick_name = mobile
    user.password_hash = password
    user.mobile = mobile
    try:
        db.session.add(user)
        db.session.commit()
        ret = "注册成功..."
    except Exception as ret:
        print("---->",ret)
        db.session.rollback()
        ret = "注册失败..."

    return ret
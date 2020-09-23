from flask import request, jsonify, session, redirect, url_for

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
        # 注册成功后，立刻认为登录成功，也就是说需要进行状态保持
        session['user_id'] = user.id
        session['nick_name'] = mobile

        ret = {
            "errno": 0,
            "errmsg": "注册成功"
        }
    except Exception as ret:
        print("---->", ret)
        db.session.rollback()
        ret = {
            "errno": 0,
            "errmsg": "注册失败..."
        }

    return jsonify(ret)


@passport_blu.route("/passport/login", methods=["GET", "POST"])
def login():
    # 1. 提取登录时的用户名，密码
    mobile = request.json.get("mobile")
    password = request.json.get("password")
    # 2.查询，如果存在表示登录成功，否则失败
    user = db.session.query(User).filter(User.mobile == mobile , User.password_hash == password).first()
    if user:
        ret = {
            "errno": 0,
            "errmsg": "登录成功"

        }
        session['user_id'] = user.id
        session['nick_name'] = mobile
    else:
        ret = {
            "errno": 0,
            "errmsg": "用户名或者密码错误"
        }

    return jsonify(ret)

@passport_blu.route("/passport/logout", methods=["GET", "POST"])
def logout():
    # 清空登录状态
    session.clear()
    return redirect(url_for('index_blu.index'))
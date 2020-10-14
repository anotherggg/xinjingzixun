import random

from flask import request, jsonify, session, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.index import User
from utils.sms_aliyun import send_msg_to_phone

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
    print(session.get("image_code"), '8' * 90)

    # 验证图片验证码是否正确
    if session.get("image_code") != image_code:
        ret = {
            "errno": 1003,
            "errmsg": "重新输入验证码"
        }
        return jsonify(ret)

    # 创建一个新用户
    # 查询是否有这个相同的用户
    if db.session.query(User).filter(User.mobile == mobile).first():
        return jsonify({
            "errno": 1001,
            "errmsg": "已经注册..."
        })

    # 注册用户为未注册用户
    # 将新用户的数据插入到数据库
    user = User()
    user.nick_name = mobile
    user.password_hash = generate_password_hash(password)
    user.mobile = mobile
    try:
        db.session.add(user)
        print('8' * 90)
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
            "errno": 1002,
            "errmsg": "注册失败..."
        }

    return jsonify(ret)


@passport_blu.route("/passport/login", methods=["GET", "POST"])
def login():
    # 1. 提取登录时的用户名，密码
    mobile = request.json.get("mobile")
    password = request.json.get("password")
    # 2.查询，如果存在表示登录成功，否则失败
    user = db.session.query(User).filter(User.mobile == mobile).first()
    print(user, '8' * 80)
    print(check_password_hash(user.password_hash, password), '9' * 80)
    if user and check_password_hash(user.password_hash, password):
        ret = {
            "errno": 0,
            "errmsg": "登录成功"

        }
        session['user_id'] = user.id
        session['nick_name'] = mobile
    else:
        ret = {
            "errno": 2001,
            "errmsg": "用户名或者密码错误"
        }

    return jsonify(ret)


@passport_blu.route("/passport/logout", methods=["GET", "POST"])
def logout():
    # 清空登录状态
    session.clear()
    return redirect(url_for('index_blu.index'))


@passport_blu.route("/passport/image_code")
def image_code():
    from utils.captcha.captcha import captcha

    # 读取一个图片
    with open("./yanzhengma.png", 'rb') as f:
        image = f.read()

    # 生成验证码
    # hash值 验证码值 图片内容
    name, text, image = captcha.generate_captcha()

    print("刚刚生成的验证码", text)

    # 通过session的方式,缓存刚刚生成的验证码，否则注册时不知道刚刚生成的是多少
    session["image_code"] = text

    # 返回响应内容
    resp = make_response(image)

    # 设置内容类型
    resp.headers['Content-Type'] = 'image/png'

    return resp


@passport_blu.route("/passport/smscode", methods=["POST"])
def smscode():
    # 1.提取数据
    mobile = request.json.get("mobile")
    image_code = request.json.get("image_code")
    # 2.校验图片验证码是否正确
    image_code_session = session.get("image_code")
    if image_code.lower() != image_code_session.lower():
        ret = {
            "errno": 4004,
            "errmsg": "图片验证码错误，请重新输入"
        }
        return jsonify(ret)
    print("短信验证码：", image_code)
    # 3.生成一个随机的6位数
    sms_code = random.randint(100000, 999999)
    # 4.存储到session中
    session["sms_code"] = sms_code
    # 5.通过短信发送这个6位数
    # send_msg_to_phone(mobile,sms_code)
    ret = {
        "errno": 0,
        "errmsg": "发送短信验证码成功..."
    }

    return jsonify(ret)

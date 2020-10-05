import hashlib
from time import ctime

from flask import jsonify, request, session, render_template, redirect, url_for
from PIL import Image
from main import basedir
from models import db
from models.index import User, Follow
from . import user_blu


@user_blu.route("/user/follow", methods=["POST"])
def follow():
    action = request.json.get("action")
    # 提取到if前面，以便在if或者else中都可以使用
    # 1. 提取当前作者的id
    news_author_id = request.json.get("user_id")

    # 2. 提取当前登录用户的id
    user_id = session.get("user_id")
    if action == "do":
        # 实现关注的流程
        # 3.判断之前是否已经关注过
        news_author = db.session.query(User).filter(User.id == news_author_id).first()
        if user_id in [x.id for x in news_author.followers]:
            return jsonify({
                "errno": 3001,
                "errmsg": "已经关注了，情勿重复关注..."
            })
        # 4. 如果未关注，则进行关注
        try:
            follow = Follow(followed_id=news_author_id, follower_id=user_id)
            db.session.add(follow)
            db.session.commit()

            ret = {
                "errno": 0,
                "errmsg": "关注成功"
            }
            return jsonify(ret)
        except Exception as ret:
            db.session.rollback()
            ret = {
                "errno": 3003,
                "errmsg": "关注失败"

            }
            return jsonify(ret)
    else:
        # 取消关注
        try:
            follow = db.session.query(Follow).filter(Follow.followed_id == news_author_id,
                                                     Follow.follower_id == user_id).first()
            db.session.delete(follow)
            db.session.commit()

            ret = {
                "errno": 0,
                "errmsg": "取消关注成功"
            }

            return jsonify(ret)

        except Exception as ret:
            db.session.rollback()
            ret = {
                "errno": 3004,
                "errmsg": "取消关注失败..."
            }

            return jsonify(ret)


@user_blu.route("/user/center")
def user_center():
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()
    nick_name = session.get("nick_name")
    # 如果用户未登录，禁止访问用户中心
    if not nick_name:
        return redirect(url_for("index_blu.index"))
    return render_template("user.html", nick_name=nick_name,user=user)


@user_blu.route("/user/user_base_info")
def user_base_info():
    return render_template("user_base_info.html")


@user_blu.route("/user/basic", methods=["POST"])
def user_basic():
    # 获取用户的新的信息
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    # 获取当前用户的信息
    user_id = session.get("user_id")

    # 存储到数据库
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
        ret = {
            "errno": 4002,
            "errmsg": "没有此用户"
        }

        return jsonify(ret)

    # 如果查询到此用户就修改数据
    user.nick_name = nick_name
    user.signature = signature
    user.gender = gender

    db.session.commit()

    ret = {
        "errno": 0,
        "errmsg": "修改成功..."
    }
    return jsonify(ret)


@user_blu.route("/user/user_pass_info")
def user_pass_info():
    return render_template("user_pass_info.html")


@user_blu.route("/user/password", methods=["POST"])
def user_password():
    # 1. 提取旧密码以及新密码
    new_password = request.json.get("new_password")
    old_password = request.json.get("old_password")

    # 2. 提取当前用户的id
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "errno": 4001,
            "errmsg": "请先登录"
        })

    # 2. 判断旧密码与数据中的当前存储的密码是否相同
    user = db.session.query(User).filter(User.id == user_id, User.password_hash == old_password).first()

    # 3. 如果相同，则修改
    if user:
        user.password_hash = new_password
        db.session.commit()
        ret = {
            "errno": 0,
            "errmsg": "修改成功"
        }

    else:
        ret = {
            "errno": 4004,
            "errmsg": "原密码错误！"
        }

    return jsonify(ret)


@user_blu.route("/user_pic", methods=["GET", "POST"])
def user_head_portrait():
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()
    if user.avatar_url:
        url = user.avatar_url
        img = open(url, "rb")
        image = img.read()
        img.close()
    else:
        img = open('./static/index/images/user_pic.png', "rb")
        image = img.read()
        img.close()
    return image

# @user_blu.route("/user/user_pic_info", methods=["GET", "POST"])
# def user_pic_info():
#     user_id = session.get("user_id")
#     user = db.session.query(User).filter(User.id == user_id).first()
#     # avatar_url = user.avatar_url
#     # print(avatar_url,'-'*50)
#     return render_template("user_pic_info.html")
#
#
# @user_blu.route("/user/avatar", methods=["POST", "POST"])
# def avatar():
#     user_id = session.get("user_id")
#     if user_id:
#         user = db.session.query(User).filter(User.id == user_id).first()
#         # avatar_url = user.avatar_url
#         avatar = request.files.get('avatar')
#         user_image = Image.open(avatar)
#         url = "./static/index/images/"
#         image_file = url + str(user.id)+'head_pic.png'
#         user.avatar_url = image_file
#         user_image.save(user.avatar_url)
#         db.session.commit()
#         ret = {
#             "errno":0,
#             "errmsg":"成功",
#             "avatar_url": image_file
#             }
#         return jsonify(ret)
#     else:
#         ret = {
#             "errno": 4002,
#             "errmsg": "失败"
#         }
#         return jsonify(ret)


@user_blu.route("/user/user_pic_info")
def user_pic_info():
    user_id = session.get("user_id")
    user = db.session.query(User).filter(User.id == user_id).first()
    return render_template("user_pic_info.html",user=user)

@user_blu.route("/user/avatar", methods=["POST"])
def user_avatar():
    f = request.files.get("avatar")
    if f:
        # 为了防止多个用户上传的图片名字相同，需要将用户的图片计算出一个随机的用户名，防止冲突
        file_hash = hashlib.md5()
        file_hash.update((f.filename+ctime()).encode("utf-8"))
        file_name = file_hash.hexdigest() + f.filename[f.filename.rfind("."):]
        avatar_url = file_name
        # 将路径改为static/upload下
        file_name = "./static/upload"+file_name
        f.save(file_name)
        # 修改数据中的用户头像链接
        user_id = session.get("user_id")
        user = db.session.query(User).filter(User.id == user_id).first()
        user.avatar_url = avatar_url
        db.session.commit()
        ret = {
            "errno": 0,
            "errmsg": "成功"
        }
    else:
        ret = {
            "errno": 4003,
            "errmsg": "上传传失败"
        }

    return jsonify(ret)









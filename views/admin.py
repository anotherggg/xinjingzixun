from flask import render_template, jsonify, request

from models import db
from models.index import Category, News
from . import admin_blu


@admin_blu.route("/admin")
def admin():
    return render_template("admin/index.html")


@admin_blu.route("/user_count.html")
def user_count():
    return render_template("admin/user_count.html")


@admin_blu.route("/user_list.html")
def user_list():
    return render_template("admin/user_list.html")


@admin_blu.route("/news_review.html")
def news_review():
    return render_template("admin/news_review.html")


@admin_blu.route("/news_edit.html")
def news_edit():
    page = int(request.args.get("page",1))
    # 分页读取
    paginate = db.session.query(News).paginate(page,5,False)
    # 获取所有的的新闻
    news = db.session.query(News).filter().all()
    return render_template("admin/news_edit.html",paginate=paginate)


@admin_blu.route("/news_edit_detail.html")
def news_edit_detail():
    # 获取需要编辑的新闻的id
    new_id = request.args.get("id")
    # 获取对应的新闻
    news = db.session.query(News).filter(News.id == new_id).first()
    # 获取新闻分类
    category = db.session.query(Category).filter(Category.id != 1).all()
    return render_template("admin/news_edit_detail.html",news=news,categorys=category)


@admin_blu.route("/admin/news_edit_detail/<int:news_id>",methods=["POST"])
def save_news(news_id):
    # 更新新闻
    news = db.session.query(News).filter(News.id == news_id).first()
    if not news:
        ret = {
            "errno": 5003,
            "errmsg": "修改失败"
        }
        return jsonify(ret)
    ret = {
        "errno":0,
        "errmsg": "修改成功"
    }
    return jsonify(ret)


@admin_blu.route("/news_type.html")
def news_type():
    news_types = db.session.query(Category).filter(Category.id != 1).all()
    return render_template("admin/news_type.html",news_types=news_types)


@admin_blu.route("/admin/news_type",methods=["POST"])
def news_type_edit():
    category_id = request.json.get("id")
    name = request.json.get("name")
    if category_id:
        one_type = db.session.query(Category).filter(Category.id == category_id).first()
        one_type.name = name
        db.session.commit()
        ret = {
            "errno":0,
            "errmsg":"修改成功"
        }
    else:
        category = Category()
        category.name = name
        db.session.add(category)
        db.session.commit()
        ret = {
            "errno": 0,
            "errmsg": "添加成功"
        }
    return jsonify(ret)
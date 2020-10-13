from flask import render_template, jsonify, request

from models import db
from models.index import Category
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
    return render_template("admin/news_edit.html")


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
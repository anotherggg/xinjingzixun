from flask import render_template, jsonify, request, session, redirect,g
from datetime import datetime,timedelta

from sqlalchemy import extract

from models import db
from models.index import Category, News, User
from . import admin_blu


@admin_blu.route("/admin")
def admin():
    # 获取用户id
    # user_id = session.get("user_id")
    # user = db.session.query(User).filter(User.id == user_id).first()
    if not g.user:
        redirect("index_blu.index")
    return render_template("admin/index.html",user=g.user)


@admin_blu.route("/user_count.html")
def user_count():
    # 获取用户人数
    total_count = db.session.query(User).count()
    # 统计当月用户新增量
    now_date = datetime.now()
    year = now_date.year
    month = now_date.month
    month_count = db.session.query(User).filter(extract('year',User.create_time) == year,
                                            extract('month',User.create_time) == month).count()
    # 统计当日用户新增量
    day = now_date.day
    day_count = db.session.query(User).filter(extract('year',User.create_time) == year,
                                            extract('month',User.create_time) == month,
                                            extract('day',User.create_time) == day).count()
    # 计算出近30天的数据
    counts_li = []
    date_li = []
    begin_date = now_date - timedelta(days=29)

    for i in range(0, 30):
        # 计算当前日期
        cur_date = begin_date + timedelta(days=i)

        # 获取当前日期的年月日
        year = cur_date.year
        month = cur_date.month
        day = cur_date.day

        # 计算出当天新增用户数量
        count = db.session.query(User).filter(extract('year', User.last_login) == year,
                                              extract('month', User.last_login) == month,
                                              extract('day', User.last_login) == day).count()

        # 把当天新增用户数量保存在counts_li列表中
        counts_li.append(count)

        # 保存当前日期
        date_str = cur_date.strftime('%Y-%m-%d')
        date_li.append(date_str)
    return render_template("admin/user_count.html",total_count=total_count,month_count=month_count,day_count=day_count,counts_li=counts_li,date_li=date_li)


@admin_blu.route("/user_list.html")
def user_list():
    page = int(request.args.get("page",1))
    # 获取用户信息
    paginate = db.session.query(User).paginate(page,5,False)
    return render_template("admin/user_list.html",paginate=paginate)


@admin_blu.route("/news_review.html")
def news_review():
    page = int(request.args.get("page",1))
    # 分页读取
    paginate = db.session.query(News).paginate(page,5,False)
    return render_template("admin/news_review.html",paginate=paginate)


@admin_blu.route("/news_review_detail.html")
def news_review_detail():
    # 获取新闻id
    news_id = request.args.get("id")
    # 获取相应的新闻内容
    new = db.session.query(News).filter(News.id==news_id).first()
    # 获取分类

    return render_template("admin/news_review_detail.html",new=new)


@admin_blu.route("/admin/news_review_detail/<int:news_id>",methods=["POST"])
def news_review_detail_s(news_id):
    # 获取当前新闻
    news = db.session.query(News).filter(News.id == news_id).first()
    if not news:
        ret = {
            "errno": 5004,
            "errmsg": "没有找到对应的新闻"
        }
        return jsonify(ret)
    action = request.json.get("action")
    if action == "accept":
        news.status = 0
    else:
        news.status = -1
    db.session.commit()
    ret = {
        "errno":0,
        "errmsg":"修改成功"
    }
    return jsonify(ret)


@admin_blu.route("/news_edit.html")
def news_edit():
    page = int(request.args.get("page",1))
    # 分页读取
    paginate = db.session.query(News).paginate(page,5,False)
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
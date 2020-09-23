from flask import render_template, jsonify, request, session

from . import index_blu

from models import db

from models.index import News


@index_blu.route("/")
def index():
    clicks_top_6_news = db.session.query(News).order_by(-News.clicks).limit(6)
    # 查询用户是否已经登录
    user_id = session.get("uesr_id",0)
    nick_name = session.get("nick_name","")
    return render_template("index.html", clicks_top_6_news=clicks_top_6_news,nick_name = nick_name)


@index_blu.route("/newslist")
def category_news():
    # 获取前端传来的数据
    page = int(request.args.get('page', 1))
    cid = int(request.args.get('cid', 0))
    per_page = int(request.args.get('per_page', 1))
    # 到数据库查询数据
    if cid == 0:
        paginate = db.session.query(News).order_by(-News.clicks).paginate(page=page, per_page=per_page, error_out=False)
    else:
        cid += 1
        paginate = db.session.query(News).filter(News.category_id == cid).paginate(page=page, per_page=per_page,
                                                                                   error_out=False)

    ret = {
        "totalPage": paginate.pages,
        "newsList": [news.to_dict() for news in paginate.items]
    }
    # for news in paginate.items:
    #     temp_dit = dict()
    #     temp_dit["id"] = news.id
    #     temp_dit["digest"] = news.digest
    #     temp_dit["create_time"] = news.create_time
    #     temp_dit["index_image_url"] = news.index_image_url
    #     temp_dit["source"] = news.source
    #     temp_dit["title"] = news.title
    #
    #     # 将得到的字典，添加到ret中newsList对应的列表中
    #     ret['newsList'].append(temp_dit)

    return jsonify(ret)


@index_blu.route("/detail/<int:news_id>")
def detail(news_id):
    clicks_top_6_news = db.session.query(News).order_by(-News.clicks).limit(6)
    # 查询用户是否已经登录
    user_id = session.get("uesr_id", 0)
    nick_name = session.get("nick_name", "")
    # 查询点击量最多的前6个新闻信息
    news = db.session.query(News).filter(News.id == news_id).first()
    return render_template("detail.html", news=news,nick_name=nick_name)

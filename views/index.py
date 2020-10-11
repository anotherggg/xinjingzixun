from flask import render_template, jsonify, request, session

from . import index_blu

from models import db

from models.index import News, Comment


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
        paginate = db.session.query(News).filter(News.status == 0).order_by(-News.create_time).paginate(page=page, per_page=per_page, error_out=False)
    else:
        cid += 1
        paginate = db.session.query(News).filter(News.category_id == cid,News.status == 0).order_by(-News.create_time).paginate(page=page, per_page=per_page,
                                                                                   error_out=False)

    ret = {
        "totalPage": paginate.pages,
        "newsList": [news.to_dict() for news in paginate.items]
    }

    return jsonify(ret)


@index_blu.route("/detail/<int:news_id>")
def detail(news_id):
    # 查询点击量最多的前6个新闻信息
    clicks_top_6_news = db.session.query(News).order_by(-News.clicks).limit(6)
    news = db.session.query(News).filter(News.id == news_id).first()
    # 查询这个新闻的作者
    news_author = news.user
    news_author.news_num = news_author.news.count()
    news_author.follwer_num = news_author.followers.count()
    # 查询用户是否已经登录
    user_id = session.get("user_id", 0)
    nick_name = session.get("nick_name", "")
    # 获取评论
    comments = news.comments.order_by(-Comment.create_time)

    # 计算当前登录用户是否已经关注了这个新闻的作者
    news_author_followers_id = [x.id for x in news_author.followers]
    if user_id in news_author_followers_id:
        news_author.can_follow = False  # 已经关注了作者，就不能在关注了
    else:
        news_author.can_follow = True  # 可以关注
    # 计算当前用户是否收藏了这篇文章
    news_collected_user_id = [x.id for x in news.collected_user]
    if user_id in news_collected_user_id:
        news.can_collect = False
    else:
        news.can_collect = True
    return render_template("detail.html", news=news,nick_name=nick_name,news_author=news_author,clicks_top_6_news=clicks_top_6_news,comments=comments)

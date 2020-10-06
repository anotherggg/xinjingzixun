from flask import jsonify, request, session

from models import db
from models.index import Collection
from . import news_blu


@news_blu.route("/news/collect", methods=["POST"])
def news_collect():
    # 1.提取参数
    news_id = request.json.get("news_id")
    action = request.json.get("action")
    # 2.获取当前用户的id
    user_id = session.get("user_id")
    # 3.判断是收藏
    if action == "do":
        collection = Collection()
        collection.news_id = news_id
        collection.user_id = user_id
        try:
            db.session.add(collection)
            db.session.commit()
            ret = {
                "errno": 0,
                "errmsg": "收藏成功"
            }
        except Exception as ret:
            ret = {
                "errno": 5001,
                "errmsg": "收藏失败"
            }
    elif action == "undo":
        collection = db.session.query(Collection).filter(Collection.user_id == user_id,
                                                         Collection.news_id == news_id).first()
        if collection:
            db.session.delete(collection)
            db.session.commit()
            ret = {
                "errno": 0,
                "errmsg": "取消收藏成功"
            }
        else:
            ret = {
                "errno": 5002,
                "errmsg": "取消收藏失败"
            }
    return jsonify(ret)

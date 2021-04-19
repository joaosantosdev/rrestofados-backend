from sqlalchemy import any_,or_,and_
from flask import request
from app import db
import json
from app.models.pagination import Pagination

class Model:
    def update(self, data,not_update=[]):
        for key, value in  data.items():
            if key in not_update:
                continue
            setattr(self, key, value)


    @classmethod
    def filter_by(cls,**kwargs):
        result = cls().query.filter_by(**kwargs).all()
        db.session.remove()
        return result

    @classmethod
    def get_all(cls,**kwargs):
        result = cls().query.all()
        db.session.remove()
        return result

    @classmethod
    def all(cls,**kwargs):
        result = cls().query.filter_by(status=any_([1,2])).all()
        db.session.remove()
        return result

    @classmethod
    def paginate_search(cls, **kwargs):
        page = request.args.get('page', 1, type=int)
        perPage = request.args.get('perPage', 10, type=int)
        search = request.args.get('search', None, type=str)

        if search:
            search = json.loads(search)
        else:
            search = dict()
        newSearch = dict()
        for key in search:
            if search.get(key,None) and search.get(key,None) is not None and search.get(key,None) != '':
                newSearch[key] = search[key]


        query = cls().query.filter_by(status=any_([1, 2])).filter_by(**newSearch)
        items = query.offset((page - 1) * perPage).limit(perPage).all()
        count = query.count()
        db.session.remove()


        return Pagination(items,count,page)

    @classmethod
    def filter(cls,**kwargs):
        result = cls().query.filter_by(**kwargs,status=any_([1, 2])).first()
        db.session.remove()
        return result


    @classmethod
    def filter_one(cls, **kwargs):
        result = cls().query.filter_by(**kwargs, status=any_([1, 2])).first()
        db.session.remove()
        return result


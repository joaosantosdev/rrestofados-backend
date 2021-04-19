from app import db

def save(tecido):
    try:
        db.session.add(tecido)
        db.session.commit()
        return tecido,None
    except Exception as e:
        return None,e.__str__()
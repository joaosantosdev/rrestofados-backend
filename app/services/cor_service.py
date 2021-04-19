from app import db



def save(cor):
    try:
        db.session.add(cor)
        db.session.commit()
        return cor,None
    except Exception as e:
        return None,e.__str__()
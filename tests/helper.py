from app.models import Character

def get_cid(db, name, *args):
    cid = db.session.query(Character).filter_by(name=name).first().id
    if args:
        return cid, db.session.query(Character).filter_by(name=args[0]).first().id
    return cid

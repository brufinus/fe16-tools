from app.models import Character

def get_cid(db, name, *args):
    if len(args) > 0:
        return (db.session.query(Character).filter_by(name=name).first().id,
                db.session.query(Character).filter_by(name=args[0]).first().id)
    return db.session.query(Character).filter_by(name=name).first().id

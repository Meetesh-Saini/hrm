from database import get_db
from werkzeug.local import LocalProxy

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


class DB:

    def add_member(self, name, reg, contact, email):
        if self.isgroup("member"):
            db.users.insert_one(
                {"name": name, "reg": reg, "contact": contact, "email": email,
                 "group": ["member"]}
            )

    def isgroup(self, group):
        x = db.groups.find({
            "name": {"$eq": group}
        })
        if len(list(x)) != 0:
            return True
        return False

    def add_group(self, group, scopeArray):
        if self.isgroup(group):
            return False
        else:
            db.groups.insert_one({
                "name": group,
                "scope": {
                    "global": scopeArray
                }
            })
            return True

    def add_scope(self, group, scopeId, scopeArray):
        if self.isgroup(group):
            res = db.groups.find_one({
                "name": {"$eq": group}
            })
            if scopeId not in res["scope"]:
                prev_scope = res["scope"]
                prev_scope[scopeId] = scopeArray
                db.groups.update_one(
                    {"name": group}, {"$set": {"scope": prev_scope}})
                return True
        return False

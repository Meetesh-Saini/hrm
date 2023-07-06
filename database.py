from pymongo import MongoClient
from flask import current_app, g
from app import app

class PermissionWrapper:
    def __init__(self, db_url):
        self.client = MongoClient(db_url)
    
    def get_database(self, db_name):
        return DatabaseWrapper(self.client[db_name])
    
    def close(self):
        self.client.close()

class DatabaseWrapper:
    valid_permissions = ["global.write", "global.read", "global.update",
                         "global.delete", "user.write", "user.read",
                         "user.update", "user.delete"]

    def __init__(self, database):
        self.db = database
    
    def check_permission(self, username, operation, scopeId="global"):
        if operation not in self.valid_permissions:
            raise ValueError("Invalid permission type")

        get_user = self.db.users.find_one({"username": {"$eq": username}})
        valid = False
        if get_user:
            for group in get_user["group"]:
                if self.check_scope(group, scopeId, operation):
                    valid = True
        return valid
    
    def get_collection(self, collection_name):
        return CollectionWrapper(self.db[collection_name], self.check_permission)
    
    def check_scope(self, group, scopeId, permission='all'):
        get_group = self.db.groups.find_one({
            "name": {"$eq": group}
        })
        if get_group:
            if scopeId in get_group["scope"]:
                all = get_group["scope"][scopeId]
                dst = {"all": all,
                        "global.write": get_group["scope"][scopeId][0],
                        "global.read": get_group["scope"][scopeId][1],
                        "global.update": get_group["scope"][scopeId][2],
                        "global.delete": get_group["scope"][scopeId][3],
                        "user.write": get_group["scope"][scopeId][4],
                        "user.read": get_group["scope"][scopeId][5],
                        "user.update": get_group["scope"][scopeId][6],
                        "user.delete": get_group["scope"][scopeId][7]
                        }
                if permission == "all":
                    return dst
                elif permission in dst:
                    return dst[permission]
                else:
                    raise NameError("Permission type not found")
        else:
            raise NameError("Group not found")


class CollectionWrapper:
    def __init__(self, collection, permission_checker):
        self.collection = collection
        self.permission_checker = permission_checker
    
    def can_perform_operation(self, username, operation, scope):
        return self.permission_checker(username, operation, scope)
    
    def find(self, username, scope, owner=False, *args, **kwargs):
        permission = "user.read" if owner else "global.read"
        if not self.can_perform_operation(username, permission, scope):
            # Handle permission denied for read operation
            raise PermissionError("Read permission denied")
        return self.collection.find(*args, **kwargs)
    
    def find_one(self, username, scope, owner=False, *args, **kwargs):
        permission = "user.read" if owner else "global.read"
        if not self.can_perform_operation(username, permission, scope):
            # Handle permission denied for read operation
            raise PermissionError("Read permission denied")
        return self.collection.find_one(*args, **kwargs)

    def insert_one(self, username, scope, document, owner=False):
        permission = "user.write" if owner else "global.write"
        if not self.can_perform_operation(username, permission, scope):
            # Handle permission denied for create operation
            raise PermissionError("Create permission denied")
        return self.collection.insert_one(document)
    
    def insert_many(self, username, scope, documents, owner=False):
        permission = "user.write" if owner else "global.write"
        if not self.can_perform_operation(username, permission, scope):
            # Handle permission denied for create operation
            raise PermissionError("Create permission denied")
        return self.collection.insert_many(documents)
    
    def update_one(self, username, scope, filter, update, owner=False, **kwargs):
        permission = "user.update" if owner else "global.update"
        if not self.can_perform_operation(username, permission, scope):
            # Handle permission denied for update operation
            raise PermissionError("Update permission denied")
        return self.collection.update_one(filter, update, **kwargs)
    
    def update_many(self, username, scope, filter, update, owner=False, **kwargs):
        permission = "user.update" if owner else "global.update"
        if not self.can_perform_operation(username, permission, scope):
            # Handle permission denied for update operation
            raise PermissionError("Update permission denied")
        return self.collection.update_many(filter, update, **kwargs)
    
    def delete_one(self, username, scope, filter, owner=False):
        permission = "user.delete" if owner else "global.delete"
        if not self.can_perform_operation(username, permission, scope):
            # Handle permission denied for delete operation
            raise PermissionError("Delete permission denied")
        return self.collection.delete_one(filter)

    def delete_many(self, username, scope, filter, owner=False):
        permission = "user.delete" if owner else "global.delete"
        if not self.can_perform_operation(username, permission, scope):
            # Handle permission denied for delete operation
            raise PermissionError("Delete permission denied")
        return self.collection.delete_many(filter)


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        with app.app_context():
            wrapper = PermissionWrapper(current_app.config["MONGO_URI"])
            # Get a specific database using the wrapper
            db = g._database = wrapper.get_database(current_app.config["MONGO_DB_NAME"])
    return db

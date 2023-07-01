## Project Name
diJAMS - Dude it's Just Another Management System

## PyMongo Docs
https://pymongo.readthedocs.io/en/stable/api/

## Permissions
C               R      U        D
[create/write, read, update, delete]
write: Write, create new element
read: view elements
update: Change existing elements
delete: Delete elements 
* Global permissions:
    * CRUD permission for entity owned by another user
    * Entity owned by none is owned by admin
* User permissions:
    * CRUD permissions for entity owned by user

## Groups and Scope
* Each user can be in multiple groups
* Each group has its scope for various software entities
* Scope defines permissions of that entity for user of that group
* Scope is 8 bits integer array:
    * Upper nibble: Global permissions
    * Lower nibble: User permissions
* Each group should contain all scopes 
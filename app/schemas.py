from marshmallow import Schema, fields

class UserToCreate(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserToUpdate(Schema):
    username = fields.Str()
    password = fields.Str(required=True)
    new_password = fields.Str()

class UserToLogin(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class PlaylistToCreate(Schema):
    name = fields.Str(required=True)
    is_public = fields.Bool(required=True)

class PlaylistToUpdate(Schema):
    name = fields.Str()
    is_public = fields.Bool()

class TrackToCreate(Schema):
    youtube_id = fields.Str(required=True)
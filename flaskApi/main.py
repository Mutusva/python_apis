from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myflask.db'
db = SQLAlchemy(app)


# models

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"


# db.create_all()

names = {"Tim": {"age": 19, "gender": "Male"},
         "Inno": {"age": 32, "gender": "Male"}}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video Required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video Required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video Required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video Required")
video_update_args.add_argument("views", type=int, help="Views of the video Required")
video_update_args.add_argument("likes", type=int, help="Likes of the video Required")

videos = {}


def abort_on_wrong_id(id):
    if id not in videos:
        abort(404, message="video of id " + str(id) + " is not valid")


# resource fields define how an object is serialised.
resource_fields = dict(id=fields.Integer, name=fields.String, views=fields.Integer, likes=fields.Integer)


class Video(Resource):

    @marshal_with(resource_fields)
    def get(self, id):
        result = VideoModel.query.filter_by(id=id).first()
        if not result:
            abort(409, message="could not find video with id " + str(id))
        return result, 200

    @marshal_with(resource_fields)
    def put(self, id):
        result = VideoModel.query.filter_by(id=id).first()
        if result:
            abort(409, "Video already exists")

        args = video_put_args.parse_args()
        video = VideoModel(id=id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201  # 201 created

    def delete(self, id):
        abort_on_wrong_id(id)
        del videos[id]
        return '', 204  # deleted

    @marshal_with(resource_fields)
    def patch(self):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=id).first()
        if not result:
            abort(409, message="could not find video with id " + str(id))
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()
        return result


api.add_resource(Video, "/video/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)

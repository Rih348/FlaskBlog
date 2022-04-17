from flask import render_template, request, Blueprint
from blog.models import Posts

main = Blueprint('main', __name__)

@main.route("/")
def home():
    page = request.args.get('page',1,type=int)
    posts = Posts.query.order_by(Posts.time.desc()).paginate(page=page , per_page=5)
    return render_template("home.html", title= "Home", posts = posts)


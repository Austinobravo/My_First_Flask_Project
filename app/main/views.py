from flask import Blueprint,request,render_template
from app.database import database
from  app.models import Post

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)#type=int
    post= Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
    # print('post',post)
    # for date in post:
    #     dates = date.date_created
    #     print(str(dates))
    #     date1= str(dates).split(' ')[1]
    #     print(date1)
    if request.method=="POST":
        data = request.form.get('search')
        db = database(data)
        return render_template("home.html", db=db)
    return render_template("blog-grid-view.html",post=post )

@main.route("/about")
def about():
    #db = database()
    return render_template("about-us.html")
@main.route("/news")
def news():
   # db = blogupload()
    return render_template("new.html", blog=db)
@main.route("/services")
def services():
    # db = database()
    return render_template("services.html")

from flask import Blueprint,flash,redirect, abort, render_template, request,url_for
from flask_login import current_user, login_required
from app import db
from app.models import Post, User
from app.posts.forms import PostForm
from app.users.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/post", methods=['GET', 'POST'])   
@login_required
def edit_post():
    form = PostForm()
    if form.is_submitted():
        post = Post(title=form.title.data,
                    description= form.description.data,                 
                    author=current_user
                   )
        image = request.files.get("image_upload")
        if image:
            print('image:', form.image_upload.data)
            print('image:', image)
            picture = save_picture(image)
            post.image_file= picture
        db.session.add(post)
        db.session.commit()
        flash('Post Updated', 'success')
        return redirect('/')
    return render_template('edit.html', form=form)

@posts.route("/post/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog-article.html', post=post)

@posts.route("/user/<string:first_name>")
def user_posts(first_name):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(first_name=first_name).first_or_404()
    post = Post.query.filter_by(author=user)\
            .order_by(Post.date_created.desc())\
            .paginate(page=page, per_page=5)
    return render_template('user.html', post=post,user=user)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def post_detail_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        form = PostForm()
        if form.is_submitted():
            post.title=form.title.data
            post.description=form.description.data
            post.image_file=form.image_upload 
            db.session.commit()
            flash('Post Updated', 'success')
            return redirect(url_for('posts.post', post_id=post.id))
        elif request.method=="GET":
            form.title.data=post.title
            form.description.data=post.description
            # form.image_upload = post.image_file
    else:
        abort(403)
    return render_template('edit.html', form=form)

@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', 'danger')
        return redirect('/  ')
            # form.image_upload = post.image_file
    else:
        abort(403)

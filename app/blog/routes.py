from app import db
from flask_login import current_user
from flask import render_template, redirect, url_for, request, abort, current_app
from app.blog.forms import PostForm
from app.models import Post, Tag
from app.blog import bp
import sqlalchemy as sa
from datetime import date
from flask_ckeditor.utils import cleanify
import math
from functools import wraps

def admin_only(function):
    @wraps(function)
    def wrapper_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=request.path))
        elif current_user.is_authenticated and current_user.id != 1:
            return abort(403)
        else:
            return function(*args, **kwargs)
    return wrapper_function


@bp.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.date.desc())
    posts = db.paginate(query, page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('blog.blog', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('blog.blog', page=posts.prev_num) \
        if posts.has_prev else None

    total_pages = math.ceil(posts.total / current_app.config['POSTS_PER_PAGE'])
    # print(posts.last, posts.first, posts.items, page)

    return render_template("blog/blog.html", title='All Articles', all_posts=posts.items,
                           next_url=next_url, prev_url=prev_url, total_pages=total_pages, current_page=page)


@bp.route('/blog/tag/<tag_name>')
def get_posts_tag(tag_name):
    query = db.select(Post).join(
        Post.tags).filter(Tag.name == tag_name)
    posts = db.paginate(query, per_page=4)
    return render_template("blog/blog.html", all_posts=posts, title=tag_name)


@bp.route("/new-post", methods=['GET', 'POST'])
@admin_only
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            name=form.author.data,
            body=cleanify(form.body.data),
            user_id=current_user.id,
            img_url=form.img_url.data,
        )

        db.session.add(new_post)
        tags_name = form.tags.data.split(' ')
        tags_name = [name for name in tags_name if name != '']

        for name in tags_name:
            query = sa.select(Tag).where(Tag.name == name)
            tag = db.session.scalar(query)

            if not tag:
                new_tag = Tag(
                    name=name
                )
                db.session.add(new_tag)
                new_post.tags.append(new_tag)
            else:
                new_post.tags.append(tag)

        db.session.commit()
        return redirect(url_for('blog.blog'))
    return render_template("blog/make-post.html", form=form, title="New Post")


@bp.route("/edit-post/<post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    tags_str = ' '.join([tag.name for tag in post.tags])
    edit_form = PostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.user.name,
        tags=tags_str,
        body=post.body
    )
    edit_form.submit.label.text = 'Edit Post'

    if edit_form.validate_on_submit():

        date_now = date.today()
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.update_date = date_now.strftime("%B %d, %Y")
        post.body = cleanify(edit_form.body.data)
        post.img_url = edit_form.img_url.data

        tags_name = edit_form.tags.data.split(' ')
        tags_name = [name for name in tags_name if name != '']

        old_tags = tags_str
        new_tags = ' '.join(tags_name)

        tags_removed = [tag for tag in old_tags if tag not in new_tags]
        tags_added = [tag for tag in new_tags if tag not in old_tags]

        if old_tags != new_tags:
            for name in tags_name:
                tag = db.session.execute(
                    db.select(Tag).where(Tag.name == name)).scalar()

                if not tag:
                    new_tag = Tag(
                        name=name
                    )
                    db.session.add(new_tag)
                    db.session.commit()
                    post.tags.append(new_tag)
                    db.session.commit()
                elif post.tags.count(tag) == 0:
                    post.tags.append(tag)
        db.session.commit()

        return redirect(url_for('blog/blog.show_post', post_id=post.id))

    return render_template("blog/make-post.html", form=edit_form, title="Edit Post")


@bp.route("/delete/<post_id>")
@admin_only
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.blog'))


@bp.route('/post/<post_id>')
def show_post(post_id):
    requested_post = db.get_or_404(Post, post_id)
    posts = Post.query.order_by(Post.id.desc()).limit(3).all()

    # print(posts)
    return render_template("blog/post.html", post=requested_post, posts=posts)


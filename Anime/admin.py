from flask import Blueprint

admin_page = Blueprint('admin', __name__)


@admin_page.route('/')
def home():
    return "Admin home page"


@admin_page.route('/user')
def user():
    return "User home page"

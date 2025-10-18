from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_admin import AdminIndexView, expose
from app.models import User
from app.forms import LoginForm  # We'll create this next

class MyAdminIndexView(AdminIndexView):
    
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()
    
    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # Handle user login
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data) and user.is_active:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('.index'))
            else:
                flash('Invalid email or password', 'danger')
        
        return render_template('admin/admin_login.html', form=form)
    
    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))

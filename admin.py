from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User
from forms import RegisterForm
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__)

@admin.route('/users')
@login_required
def users():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.home'))

    users = User.query.all()
    return render_template('users.html', users=users)

@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('admin.users'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('admin.add_user'))

        new_user = User(
            username=form.username.data,
            role=form.role.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('edit_user.html', form=form, title='Add User')

@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('admin.users'))

    user = User.query.get_or_404(user_id)
    form = RegisterForm(obj=user)
    form.password.validators = []  # Remove password requirement for editing
    form.confirm_password.validators = []

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user and existing_user.id != user_id:
            flash('Username already exists.', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))

        user.username = form.username.data
        user.role = form.role.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('edit_user.html', form=form, title='Edit User', user=user)

@admin.route('/users/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('admin.users'))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.users'))

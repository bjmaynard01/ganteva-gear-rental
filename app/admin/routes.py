from flask import render_template, session, url_for, redirect, flash
from app import db
from app.admin import bp as admin_bp
from app.users import utils
from flask_login import current_user
from app.users.models import User
from app.gear.models import GearCategories, GearItem
from app.gear.forms import GearItemForm, GearCategoryForm
from sqlalchemy.exc import SQLAlchemyError

@admin_bp.route('/admin')
def admin():
    
    if not current_user.is_anonymous:
    
        if current_user.is_admin == True:
            return render_template('admin/admin.html', title='Admin Panel'), 200
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
    
    else:
        return redirect(url_for('users.login'))
    
@admin_bp.route('/admin/gear')
def gear_admin():
    if not current_user.is_anonymous:

        if current_user.is_admin == True:
            return render_template('admin/admin_gear.html', title='Gear Admin'), 200
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
    else:
        return redirect(url_for('users.login'))

@admin_bp.route('/admin/gear/categories')
def categories_admin():

    if not current_user.is_anonymous:
    
        if current_user.is_admin == True:
            categories = GearCategories.query.all()
            return render_template('admin/admin_categories.html', title='Gear Categories', categories=categories), 200
    
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
    
    else:
        return redirect(url_for('users.login'))
    
@admin_bp.route('/admin/gear/categories/add', methods=['GET', 'POST'])
def add_gear_category():

    if not current_user.is_anonymous:

        if current_user.is_admin == True:
            add_category_form = GearCategoryForm()

            if add_category_form.validate_on_submit():
                name = add_category_form.name.data.capitalize()
                desc = add_category_form.desc.data.capitalize()

                try:
                    category = GearCategories(name=name, description=desc)
                    db.session.add(category)
                    db.session.commit()
                    flash(f'Successfully added gear category {name}')
                    return redirect(url_for('admin.categories_admin'))

                except SQLAlchemyError as error:
                    db.session.rollback()
                    return render_template('errors/500.html', title='Internal Error'), 500
            
            return render_template('admin/add_category.html', title='Add Category', form=add_category_form)
        
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
        
    else: return redirect(url_for('main.index'))
    
@admin_bp.route('/admin/gear/add', methods=['GET', 'POST'])
def add_gear():
    
    if not current_user.is_anonymous:

        if current_user.is_admin == True:
            add_gear_form = GearItemForm()

            if add_gear_form.validate_on_submit():
                gear_name = add_gear_form.item_name.data.capitalize()
                gear_image = add_gear_form.item_image.data
                gear_care = add_gear_form.item_care.data
                gear_qty = add_gear_form.qty.data
                geat_categories = add_gear_form.categories.data


            return render_template('admin/add_gear.html', title='Add Gear Item', form=add_gear_form)
        
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
    
    else:
        return redirect(url_for('users.login'))
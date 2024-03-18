from flask import render_template, url_for, redirect, flash
from app import db
from app.admin.gear import bp as admin_gear_bp
from flask_login import current_user, login_required
from app.gear.models import GearCategories, GearItem
from app.gear.forms import GearItemForm, GearCategoryForm, UpdateGearCategoryForm
from sqlalchemy.exc import SQLAlchemyError
from app.admin.gear.utils import save_img

@admin_gear_bp.route('/admin/gear')
@login_required
def gear_admin():
    if not current_user.is_anonymous:

        if current_user.is_admin == True:
            items = GearItem.query.all()
            return render_template('admin/gear/admin_gear.html', title='Gear Admin', items=items), 200
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
    else:
        flash('You must login to administer gear.')
        return redirect(url_for('users.login'))
    
@admin_gear_bp.route('/admin/gear/add', methods=['GET', 'POST'])
@login_required
def add_gear():
    
    if not current_user.is_anonymous:

        if current_user.is_admin == True:
            add_gear_form = GearItemForm()

            if add_gear_form.validate_on_submit():

        
                gear_name = add_gear_form.name.data.capitalize()
                gear_care = add_gear_form.care_instructions.data
                gear_qty = add_gear_form.qty.data
                gear_categories = add_gear_form.categories.data
    
                if add_gear_form.image.data:
                    picture_file, thumb_file = save_img(add_gear_form.image.data)
                    gear_image = picture_file
                    gear_thumb = thumb_file
                    
                else:
                    gear_image = None
                

                try:
                    item = GearItem(name=gear_name, image=gear_image, img_thumb=gear_thumb, care_instructions=gear_care, qty=gear_qty)

                    for category in gear_categories:
                        item.categories.append(category)
                    
                    db.session.add(item)
                    db.session.commit()
                    
                    flash(f"New gear item added: {gear_name}")
                    return redirect(url_for('admin_gear.gear_admin'))
                
                except SQLAlchemyError as error:
                    return render_template('errors/500.html', title='Internal Error'), 500

            return render_template('admin/gear/add_gear.html', title='Add Gear Item', form=add_gear_form)
        
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
    
    else:
        flash('You must login to add gear items.')
        return redirect(url_for('users.login'))
    
@admin_gear_bp.route('/admin/gear/<id>/update')
@login_required
def update_item(id):
    return redirect(url_for('admin_gear.gear_admin'))

@admin_gear_bp.route('/admin/gear/<id>/delete')
@login_required
def delete_item(id):
    return redirect(url_for('admin_gear.gear_admin'))
    
@admin_gear_bp.route('/admin/gear/categories')
@login_required
def categories_admin():

    if not current_user.is_anonymous:
    
        if current_user.is_admin == True:
            query = GearCategories.query.all()
            categories = {}
            for category in query:
                items = category.items.all()
                category_items = 0
                for item in items:
                    category_items += item.qty
                categories[category] = category_items
            

            flash(categories)
            return render_template('admin/gear/admin_categories.html', 
                                   title='Gear Categories', categories=categories, category_items=category_items), 200
    
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
    
    else:
        flash('You must login to administer gear categories')
        return redirect(url_for('users.login'))
    
@admin_gear_bp.route('/admin/gear/category/add', methods=['GET', 'POST'])
@login_required
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
                    return redirect(url_for('admin_gear.categories_admin'))

                except SQLAlchemyError as error:
                    db.session.rollback()
                    return render_template('errors/500.html', title='Internal Error'), 500
            
            return render_template('admin/gear/add_category.html', title='Add Category', form=add_category_form,
                                   legend='Add Gear Category')
        
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
        
    else: 
        flash('You must login to add gear categories')
        return redirect(url_for('users.login'))

@admin_gear_bp.route('/admin/gear/category/<id>/update', methods=['GET', 'POST'])
@login_required
def update_category(id):
    if not current_user.is_anonymous:

        if current_user.is_admin:
            try:
                category = GearCategories.query.get_or_404(id)

            except SQLAlchemyError as error:
                return render_template('errors/500.html', title='Internal Error'), 500

            form = UpdateGearCategoryForm()
        
            if form.validate_on_submit():
                category.name = form.name.data.capitalize()
                category.description = form.desc.data.capitalize()
                db.session.commit()
                flash('Successfully updated category {}'.format(category.name))
                return redirect(url_for('admin_gear.categories_admin'))
        
            form.name.data = category.name
            form.desc.data = category.description
                
            return render_template('admin/gear/add_category.html', title='Update Category', form=form,
                                       legend='Update Category'), 200
            
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
        
    else:
        flash('You must login to update gear categories.')
        return redirect(url_for('users.login'))
    
@admin_gear_bp.route('/admin/gear/category/<id>/delete')
@login_required
def delete_category(id):
    if not current_user.is_anonymous:

        if current_user.is_admin:
            
            try:
                category = GearCategories.query.get_or_404(id)
                db.session.delete(category)
                db.session.commit()
                flash('Succesfully deleted category {}'.format(category.name))
                return redirect(url_for('admin_gear.categories_admin'))
    
            except SQLAlchemyError as error:
                db.session.rollback()
                return render_template('errors/500.html', title='Internal Error'), 500
            
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
        
    else:
        flash('You must login to delete gear categories.')
        return redirect(url_for('users.login'))
                
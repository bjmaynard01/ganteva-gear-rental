from flask import render_template, url_for, redirect, flash, current_app
from app import db
from app.admin.gear import bp as admin_gear_bp
from flask_login import current_user, login_required
from app.gear.models import GearCategories, GearItem
from app.gear.forms import GearItemForm, GearCategoryForm, UpdateGearCategoryForm, UpdateGearItemForm
from sqlalchemy.exc import SQLAlchemyError
from app.admin.gear.utils import save_img, delete_gear_img, get_item_img_path
import os

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

                gear_name = add_gear_form.name.data.title()
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

            return render_template('admin/gear/add_gear.html', title='Add Gear Item', form=add_gear_form, legend='Add Gear')
        
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
    
    else:
        flash('You must login to add gear items.')
        return redirect(url_for('users.login'))
    
@admin_gear_bp.route('/admin/gear/<id>/update', methods=['GET', 'POST'])
@login_required
def update_item(id):
    if not current_user.is_anonymous:

        if current_user.is_admin:
            try:
                item = GearItem.query.get_or_404(id)

            except SQLAlchemyError as error:
                return render_template('errors/500.html', title='Internal Error'), 500

            update_gear_form = UpdateGearItemForm(item.name)

            
        
            if update_gear_form.validate_on_submit():
                item.name = update_gear_form.name.data.title()
                if update_gear_form.image.data:
                    delete_gear_img(item.image, item.img_thumb)
                    picture_file, thumb_file = save_img(update_gear_form.image.data)
                    gear_image = picture_file
                    gear_thumb = thumb_file
                    item.image = gear_image
                    item.img_thumb = gear_thumb
                item.care_instructions = update_gear_form.care_instructions.data
                item.qty = update_gear_form.qty.data
                item.categories = update_gear_form.categories.data
                try:
                    db.session.add(item)
                    db.session.commit()
                    flash('Successfully updated item {}'.format(item.name))
                    return redirect(url_for('admin_gear.gear_admin'))
                except SQLAlchemyError as error:
                    return render_template('errors/500.html', title='Internal Error'), 500
        
            update_gear_form.name.data = item.name
            update_gear_form.care_instructions.data = item.care_instructions
            update_gear_form.qty.data = item.qty
            update_gear_form.categories.data = item.categories
                
            return render_template('admin/gear/add_gear.html', title='Update Item', form=update_gear_form,
                                       legend='Update Item', item=item), 200
            
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
        
    else:
        flash('You must login to update gear categories.')
        return redirect(url_for('users.login'))

@admin_gear_bp.route('/admin/gear/<id>/delete')
@login_required
def delete_item(id):
    if not current_user.is_anonymous:

        if current_user.is_admin:
            
            try:
                item = GearItem.query.get_or_404(id)
                img_file = item.image
                img_thumb = item.img_thumb
                db.session.delete(item)
                db.session.commit()
                delete_gear_img(img_file, img_thumb)
                flash('Successfully deleted item {}'.format(item.name))
                return redirect(url_for('admin_gear.gear_admin'))
    
            except SQLAlchemyError as error:
                db.session.rollback()
                return render_template('errors/500.html', title='Internal Error'), 500
            
        else:
            return render_template('errors/401.html', title='Unauthorized'), 401
        
    else:
        flash('You must login to delete gear categories.')
        return redirect(url_for('users.login'))
    
@admin_gear_bp.route('/admin/gear/categories')
@login_required
def categories_admin():

    if not current_user.is_anonymous:
    
        if current_user.is_admin == True:
            categories = GearCategories.query.all()

            #need a join statement that pulls and adds up qtys of items and displays, but not required

            return render_template('admin/gear/admin_categories.html', 
                                   title='Gear Categories', categories=categories), 200
    
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
                name = add_category_form.name.data.title()
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

            form = UpdateGearCategoryForm(category.name)
        
            if form.validate_on_submit():
                category.name = form.name.data.title()
                category.description = form.desc.data.capitalize()
                flash(f"{form.name.data.title()} --- {category.name.title()}")
                #db.session.commit()
                #flash('Successfully updated category {}'.format(category.name))
                #return redirect(url_for('admin_gear.categories_admin'))
        
            form.name.data = category.name
            form.desc.data = category.description
                
            return render_template('admin/gear/add_category.html', title='Update Category', form=form,
                                       legend='Update Category', category=category), 200
            
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
                
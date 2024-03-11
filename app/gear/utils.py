from app.gear.models import GearCategories

def get_category_names():
    #categories = GearCategories.query.with_entities(GearCategories.name).all()
    categories = GearCategories.query.all()
    return categories  
import flask
from flask import request, jsonify
from . import db_session
from .products import Product
from .reviews import UserReview
from sqlalchemy import func

blueprint = flask.Blueprint(
    'products_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    
    db_sess = db_session.create_session()

    if category:
        products = db_sess.query(Product).filter(Product.prod_category == category).order_by(func.random()).limit(8).all()
    else:
        products = db_sess.query(Product).order_by(func.random()).limit(8).all()

    products_list = [product.to_dict() for product in products]
    return jsonify({'products': products_list})


@blueprint.route('/api/catalog', methods=['GET'])
def filter_catalog():
    db_sess = db_session.create_session()
    category_map = {
        "snacks": "Закуски",
        "cocktails": "Коктейли",
        "bitters": "Настойки",
        "non_alcoholic": "Безалкогольное"
    }

    requested_categories = request.args.getlist('category')
    categories = [category_map[cat] for cat in requested_categories if cat in category_map]

    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    order_by = request.args.get('order_by', default=None, type=str)

    query = db_sess.query(Product)

    print(f"Requested Categories: {requested_categories}")
    print(f"Mapped Categories: {categories}")
    print(f"Min Price: {min_price}, Max Price: {max_price}")
    print(f"Order By: {order_by}")

    if categories:
        query = query.filter(Product.prod_category.in_(categories))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if order_by == 'popular':
        query = query.order_by(Product.prod_id.asc())
    elif order_by == 'cheaper':
        query = query.order_by(Product.price)
    elif order_by == 'expensive':
        query = query.order_by(Product.price.desc())
    elif order_by == 'new':
        query = query.order_by(Product.prod_id.desc())

    products = query.all()
    
    print(f"Found Products: {len(products)}")
    
    products_data = [product.to_dict() for product in products]

    return jsonify({'success': True, 'products': products_data})


@blueprint.route('/api/review', methods=['DELETE'])
def delete_review():
    review_id = request.args.get('review_id', type=int)
    
    if review_id is None:
        return jsonify({"error": "review_id is required"}), 400

    # Создаем сессию базы данных
    db_sess = db_session.create_session()
    
    # Находим отзыв по review_id
    review = db_sess.query(UserReview).get(review_id)
    
    if review is None:
        return jsonify({"error": "Отзыв не найден"}), 404

    db_sess.delete(review)
    db_sess.commit()

    db_sess.close()

    return jsonify({"message": "Отзыв успешно удален"}), 200
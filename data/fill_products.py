import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from .db_session import SqlAlchemyBase, create_session 
from .products import Product  

def fill_products_from_csv(csv_file_path):
    """
    :param csv_file_path: Путь к CSV-файлу.
    """
    
    session = create_session()

    try:
        
        df = pd.read_csv(csv_file_path, sep=';', encoding='utf-8')

        for index, row in df.iterrows():
            
            product = Product(
                prod_name=row['Название'],
                price=row['Цена (руб)'],
                prod_volume=row['Объём (мл/г)'],
                prod_category=row['Категория'],
                description=row['Состав'],
                img_prod=row['Фото (название файла)']
            )

            session.add(product)

        session.commit()

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        session.rollback()
    
    finally:
        session.close()


# fill_products_from_csv('C:\Users\1\Desktop\программирование\Веб-разработка\Курсовая 2 и проект\продукты1.csv')

from app.db import get_db
from app.models import Activity, Build, Organization


db = next(get_db())
def create_data_activity():

    main_act = Activity(name='Еда', level=0, parent_id=None)
    db.add(main_act)
    db.commit()

    child1 = Activity(name='Мясная продукция', level=1, parent_id=main_act.id)
    child2 = Activity(name='Молочная продукция', level=1, parent_id=main_act.id)
    db.add(child1)
    db.add(child2)
    db.commit()

    main_act1 = Activity(name='Автомобили', level=0, parent_id=None)
    db.add(main_act1)
    db.commit()

    main_act1_child1 = Activity(name='Грузовые', level=1, parent_id=main_act1.id)
    main_act1_child2 = Activity(name='Легковые', level=1, parent_id=main_act1.id)
    db.add(main_act1_child1)
    db.add(main_act1_child2)
    db.commit()

    main_act1_child1_child1 = Activity(name='Запчасти', level=2, parent_id=main_act1_child1.id)
    main_act1_child2_child2 = Activity(name='Аксессуары', level=2, parent_id=main_act1_child1.id)
    main_act1_child1_child1_1 = Activity(name='Запчасти', level=2, parent_id=main_act1_child2.id)
    main_act1_child2_child2_1 = Activity(name='Аксессуары', level=2, parent_id=main_act1_child2.id)

    db.add(main_act1_child1_child1)
    db.add(main_act1_child2_child2)
    db.add(main_act1_child1_child1_1)
    db.add(main_act1_child2_child2_1)
    db.commit()


    # main_act1_child2_child2_7 = Activity(name='Необыкновенные', level=3, parent_id=main_act.id)

    db.add(child1)
    db.add(child2)
    db.add(main_act1)
    db.add(main_act1_child1)
    db.add(main_act1_child2)
    db.add(main_act1_child1_child1)
    db.add(main_act1_child2_child2)
    db.commit()
    # db.add(main_act1_child2_child2_7)
    # db.commit()


def create_orgs():

    build = Build(address="г. Москва, ул. Ленина 1, офис 3", coords=(55.978498, 37.173355))
    db.add(build)
    db.commit()

    org = Organization(
        name="ООО 'Рога и Копыта'",
        phone_number=['2-222-222', '3-333-333', '8-923-666-13-13'],
        build=build.id
    )

    activities = db.query(Activity).filter(Activity.id.in_([2, 3])).all()

    org.activities.extend(activities)
    db.add(org)
    db.commit()

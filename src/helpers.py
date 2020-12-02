def get_or_create(session, model, **kwargs):
    # Custom get or create instance of Model with kwargs
    # Note: DOES NOT COMMIT
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance

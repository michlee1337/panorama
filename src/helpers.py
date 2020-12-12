def get_or_create(session, model, **kwargs):
    # Custom get or create instance of Model with kwargs
    ## Checks to see if a model instance with given arguments exist
    ## If none, create a new instance with given arguments in current db session

    # !!Note: it DOES NOT COMMIT the instance creation,
    ## That should be handled in the business logic.
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance

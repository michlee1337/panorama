"""
Application-wide helper functions

Functions:

    get_or_create(db.session, class, **kwargs) -> object

"""

def get_or_create(session, model, **kwargs):
    """
    Creates and returns an instance of the model with given kwargs,
    if it does not yet exist. Otherwise, get instance and return.
        Parameters:
            session: Current database session
            model: The Class of the database model
            **kwargds: The attributes for the desired instance

        Returns:
            (object): An object instance of the model with given kwargs
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance

# TODO: Replace with custom inits

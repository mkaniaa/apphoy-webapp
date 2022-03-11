def get_field_names(model, exclude):
    """
    Returns the field names of the given model excluding those whose names
    were passed in the "exclude" parameter list.
    """
    exclude = [field_name.lower() for field_name in exclude]
    return [
        field.name
        for field in model._meta.get_fields()
        if field.name.lower() not in exclude
    ]


def get_verbose_field_names(model, exclude):
    """
    Returns the verbose field names of the given model excluding those whose
    verbose names were passed in the "exclude" parameter list.
    """
    exclude = [field_name.lower() for field_name in exclude]
    names = []
    for field in model._meta.get_fields():
        try:
            if field.verbose_name.lower() not in exclude:
                names.append(field.verbose_name)
        except AttributeError:
            continue
    return names

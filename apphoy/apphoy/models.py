def get_field_names(model, exclude=None):
    exclude = exclude if exclude else []
    return [
        field.name
        for field in model._meta.get_fields()
        if field.name not in exclude
    ]


def get_verbose_field_names(model, exclude=None):
    exclude = exclude if exclude else []
    return [
        field.verbose_name
        for field in model._meta.get_fields()
        if field.verbose_name not in exclude
    ]
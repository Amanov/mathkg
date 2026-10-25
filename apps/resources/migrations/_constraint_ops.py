"""Add or drop a unique constraint only when the database needs it.

``0043`` used to add these constraints in the same transaction as the
dedupe. Production never recorded that migration. A database that did
apply the old file already has the constraint, so adding it again would
fail. SQLite rebuilds the table from the historical model's ``_meta``,
which does not yet list a constraint added via ``SeparateDatabaseAndState``,
so the constraint is attached to ``_meta`` before ``add_constraint``.
"""

def constraint_names(schema_editor, model):
    with schema_editor.connection.cursor() as cursor:
        found = schema_editor.connection.introspection.get_constraints(
            cursor, model._meta.db_table,
        )
    return set(found)


def add_if_missing(apps, schema_editor, model_name, constraint):
    model = apps.get_model('personal', model_name)
    if constraint.name in constraint_names(schema_editor, model):
        return
    if not any(item.name == constraint.name for item in model._meta.constraints):
        model._meta.constraints.append(constraint)
    schema_editor.add_constraint(model, constraint)


def drop_if_present(apps, schema_editor, model_name, constraint):
    model = apps.get_model('personal', model_name)
    if constraint.name not in constraint_names(schema_editor, model):
        return
    model._meta.constraints = [
        item for item in model._meta.constraints if item.name != constraint.name
    ]
    schema_editor.remove_constraint(model, constraint)

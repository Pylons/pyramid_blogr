from wtforms import Form, BooleanField, TextField, TextAreaField, validators
from wtforms import HiddenField

strip_filter = lambda x: x.strip() if x else None

class BlogCreateForm(Form):
    title = TextField('Entry title', [validators.Length(min=1, max=255)],
                      filters=[strip_filter])
    body = TextAreaField('Entry body', [validators.Length(min=1)],
                         filters=[strip_filter])

class BlogUpdateForm(BlogCreateForm):
    id = HiddenField()
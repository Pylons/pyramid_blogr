from wtforms import Form, StringField, TextAreaField, validators
from wtforms import HiddenField

strip_filter = lambda x: x.strip() if x else None

class BlogCreateForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    body = TextAreaField('Contents', [validators.Length(min=1)],
                         filters=[strip_filter])

class BlogUpdateForm(BlogCreateForm):
    id = HiddenField()

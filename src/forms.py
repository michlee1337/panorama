from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField, PasswordField, FieldList, FormField, SelectMultipleField
from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from src.models.users import User
# from src.models.chunks import Chunk
from src.models.artifacts import Artifact, Chunk, Source
# from src.models.sources import Source

# _____ FIELDS ______

# Credit to M0r13n
## https://gist.github.com/M0r13n/71655c53b2fbf41dc1db8412978bcbf9
class CommaSepListField(StringField):
    """Stringfield for a list of separated tags"""

    def __init__(self, label='', validators=None, remove_duplicates=True, to_lowercase=True, separator=' ', **kwargs):
        """
        Construct a new field.
        :param label: The label of the field.
        :param validators: A sequence of validators to call when validate is called.
        :param remove_duplicates: Remove duplicates in a case insensitive manner.
        :param to_lowercase: Cast all values to lowercase.
        :param separator: The separator that splits the individual tags.
        """
        super(CommaSepListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.to_lowercase = to_lowercase
        self.separator = separator
        self.data = []

    def _value(self):
        if self.data:
            return u', '.join([str(x) for x in self.data])
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = filter(None, [x.strip() for x in valuelist[0].split(self.separator)])
            if self.remove_duplicates:
                self.data = list(self._remove_duplicates(self.data))
            if self.to_lowercase:
                self.data = [x.lower() for x in self.data]

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

# _____ FORMS _____
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Username is required")])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    login = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ChunkForm(ModelForm):
    class Meta:
        model = Chunk
    concept = StringField('Concept', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

class SourceForm(ModelForm):
    class Meta:
        model = Source
    name = StringField('Name', render_kw={"placeholder": "Name"})
    link = StringField('Link', render_kw={"placeholder": "Link"})

class ArtifactForm(ModelForm):
    class Meta:
        model = Artifact

    prerequisites = CommaSepListField(
        "Prerequisites",
        separator=",",
        to_lowercase=True
    )
    concept = StringField('Main Concept', validators=[DataRequired()])
    source = FormField(SourceForm)
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    mediatype = SelectField('Mediatype', choices=Artifact.mediatype_options(), validators=[DataRequired()], coerce=int)
    duration = SelectField('Duration', choices=Artifact.duration_options(), validators=[DataRequired()], coerce=int)
    vote_count = IntegerField()
    vote_sum = IntegerField()
    chunks = ModelFieldList(FormField(ChunkForm), min_entries=1)
    create = SubmitField('Create')

class SearchForm(FlaskForm):
    title = StringField('Title')
    concept = StringField('Main Concept')
    sub_concepts = CommaSepListField('Sub-Concepts', to_lowercase=True)
    mediatype = MultiCheckboxField('Mediatype', choices=[(0, 'Unknown'), (1, 'Text'), (2, 'Video'), (3, 'Other')])
    duration = MultiCheckboxField('Duration', choices=[(0, 'Unknown'), (1, 'Minutes'), (2, 'Days'), (3, 'Days'), (4, 'Months'), (5, 'Long')])
    search = SubmitField('Search')

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateField, IntegerField, FileField, SelectMultipleField, widgets
from wtforms.validators import Email, InputRequired, Length, NumberRange

from models.materials import Materials


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class AddError(FlaskForm):
    """Form for adding error"""

    part_number = StringField("Nest/Part Number")
    description = StringField("Description", validators=[InputRequired(message='Please enter a description')])
    machine = SelectField("Machine", choices=['Laser - Amada', 'Laser - Trumpf', 'Forming - Amada', 'Forming - Salvagnini', 'Other - Punch', 'Other'])
    root_cause = StringField("Root Cause")
    notes = TextAreaField("Notes", render_kw={'class': 'form-control', 'rows': 5})
    name = StringField("Your Name", validators=[InputRequired(message='Please enter your name')])


class EditError(FlaskForm):
    """Form for adding error"""

    part_number = StringField("Nest/Part Number")
    description = StringField("Description", validators=[InputRequired(message='Please enter a description')])
    machine = SelectField("Machine", choices=['Laser - Amada', 'Laser - Trumpf', 'Forming - Amada', 'Forming - Salvagnini', 'Other - Punch', 'Other'])
    root_cause = StringField("Root Cause")
    notes = TextAreaField("Notes", render_kw={'class': 'form-control', 'rows': 5})
    name = StringField("Your Name", validators=[InputRequired(message='Please enter your name')])


class AddRequest(FlaskForm):
    """Form for adding request"""
    
    to_change = StringField(
        "Part/Program", validators=[InputRequired(message='Please enter a part or program to change/request')])
    description = StringField("Description", validators=[InputRequired(message='Please enter a description. Quantity, Sheet Size, etc.')])
    requested_by = StringField("Name", validators=[InputRequired(message='Please enter your name')])
    request_type = SelectField("Type", choices=['Part Request', 'Laser Change', 'Forming Change'])


class SignupForm(FlaskForm):
    """Form for a user to sign-up"""

    first_name = StringField("First Name", validators=[InputRequired(
        message='Please enter your name'), Length(min=2, max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(
        message='Please enter your name'), Length(min=2, max=30)])
    email = StringField("Email", validators=[
                        InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(message='You must enter a password'), Length(
        min=6, message="Password must be at least 6 characters in length")])


class LoginForm(FlaskForm):
    """Form for user to login"""

    email = StringField("Bluestar Username/Email", validators=[
                        InputRequired(), Email(granular_message=True)])
    password = PasswordField("Password", validators=[InputRequired(message='You must enter a password'), Length(
        min=6, message="Password must be at least 6 characters in length")])


class ProjectForm(FlaskForm):
    """Form for new project"""

    project_name = StringField("Project Name", validators=[InputRequired(
        message='Please enter a name'), Length(min=2, max=60)])
    project_type = SelectField("Type", validators=[InputRequired(
        message='Please select a project type')], choices=['New model launch', 'Modify existing model', 'Other'])
    product_line = MultiCheckboxField("Product Line", choices=['Cooking', 'Refrigeration', 'Ventilation'])
    eco = StringField("ECO #")
    notes = StringField("Notes")
    date_requested = DateField(
        "Projected Completion Date", validators=[InputRequired(message='Please enter a completion date')])


class EditProjectForm(FlaskForm):
    """Form for editing project"""

    project_name = StringField("Project Name", validators=[InputRequired(
        message='Please enter a name'), Length(min=2, max=60)])
    project_type = SelectField("Type", validators=[InputRequired(
        message='Please select a project type')], choices=['New model launch', 'Modify existing model', 'Other'])
    product_line = MultiCheckboxField("Product Line", choices=['Cooking', 'Refrigeration', 'Ventilation'])
    eco = StringField("ECO #")
    notes = StringField("Notes")
    date_requested = DateField(
        "Projected Completion Date", validators=[InputRequired(message='Please enter a completion date')])
    progress = IntegerField("Progress", validators=[NumberRange(
        min=0, max=100, message="Must be between 0-100")])


class PartForm(FlaskForm):
    """Form for new part"""
    part_number = StringField("Part Number", validators=[InputRequired(
        message='Please enter a number'), Length(min=2, max=60)])
    description = StringField("Description")
    material = SelectField("Material", choices=[])
    processes = MultiCheckboxField('Processes Required. Check all that apply', choices=[
        'Punch', 'Form', 'Weld', 'Polish', 'Paint', 'Assembly', 'Enamel', 'FAV', 'Other'])
    #processes = StringField("Processes Required (Separate by ',')")
    bin_location = StringField("Bin Location")
    status = StringField("Status")
    notes = StringField("Notes")


class EditPartForm(FlaskForm):
    """Form for editing part"""

    part_number = StringField("Part Number", validators=[InputRequired(
        message='Please enter a number'), Length(min=2, max=60)])
    description = StringField("Description")
    material = StringField("Material")
    processes = MultiCheckboxField('Processes Required. Check all that apply', choices=[
        'Punch', 'Form', 'Weld', 'Polish', 'Paint', 'Assembly', 'Enamel', 'FAV', 'Other'])

    #processes = StringField("Processes Required (Separate by ',')")
    bin_location = StringField("Bin Location")
    status = StringField("Status")
    notes = StringField("Notes")


class AddFileForm(FlaskForm):
    """Form for adding file"""

    file = FileField()
    description = StringField("Description")
    notes = StringField("Notes")


class CreateIssueForm(FlaskForm):
    """Form for adding bug or request"""

    title = StringField("Title", validators=[InputRequired(
        message='Please add a title')])
    body = TextAreaField("Description", validators=[InputRequired(
        message='Please add a description of bug/request')])


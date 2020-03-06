import time
import uuid
from flask import Blueprint, render_template, request, redirect, url_for
from .forms import DescriptionForm
from ...utils import read_js, save_data, get_object_by_id
from ...github_utils import update_file


description_bp = Blueprint('description', __name__, url_prefix='/description')
data_path = 'app/data/description.js'
key = 'descriptions'
github_path = 'https://api.github.com/repos/ddehueck/ddehueck.github.io/contents/data/description.js'


@description_bp.route('/', methods=['GET', 'POST'])
def index():
    """
     GET: Display entries and form
     POST: Creates new entry
     """
    form = DescriptionForm()
    saved_data = read_js(data_path)["data"]

    # Validate incoming form data
    if form.validate_on_submit():
        saved_data.append({
            "description": form.description.data,
            "created_at": time.time(),
            "id": str(uuid.uuid4()),
        })

        save_data(saved_data, data_path, key)
        return redirect(url_for('.index'))

    if form.errors:
        print(form.errors)

    # Display standard page
    return render_template(
        'description/index.html',
        data=sorted(saved_data, key=lambda k: k['created_at'], reverse=True),
        form=form,
        title='Description Manager'
    )


@description_bp.route('/update-github', methods=['GET'])
def update_github():
    """
     GET: Pushes saved data to github using GitHub API
     """
    response = update_file(data_path, github_path)
    print(response)
    print(response.content)
    return redirect(url_for('.index'))


@description_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    """
     GET: Display entry data in form
     POST: Updates entry
     """
    form = DescriptionForm()
    saved_data = read_js(data_path)["data"]
    entry_to_edit = get_object_by_id(saved_data, id)

    # Validate incoming form data
    if form.validate_on_submit():
        # Remove old item
        saved_data.remove(entry_to_edit)
        # Add updated item
        saved_data.append({
            "description": form.description.data,
            "last_updated": time.time(),
            # Static fields below
            "created_at": entry_to_edit['created_at'],
            "id": entry_to_edit['id'],
        })

        save_data(saved_data, data_path, key)
        return redirect(url_for('.index'))

    if form.errors:
        print(form.errors)

    # Display form with prefilled data
    form.description.data = entry_to_edit.get('description', '')

    return render_template(
        'description/edit.html',
        data=entry_to_edit,
        form=form,
        title='Edit Description Entry'
    )


@description_bp.route('/delete/<id>', methods=['GET'])
def delete(id):
    """
     GET: Removes entry
     """
    # Select paper
    saved_data = read_js(data_path)["data"]
    entry_to_del = get_object_by_id(saved_data, id)

    # Remove and save!
    saved_data.remove(entry_to_del)
    save_data(saved_data, data_path, key)

    return redirect(url_for('.index'))

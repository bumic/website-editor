import time
import uuid
from flask import Blueprint, render_template, request, redirect, url_for
from .forms import SummaryForm
from ...utils import read_js, save_data, get_object_by_id
from ...github_utils import update_file


summary_bp = Blueprint('summary', __name__, url_prefix='/summary')
data_path = 'app/data/summary.js'
key = 'summarys'
github_path = 'https://api.github.com/repos/ddehueck/ddehueck.github.io/contents/data/summary.js'


@summary_bp.route('/', methods=['GET', 'POST'])
def index():
    """
     GET: Display entries and form
     POST: Creates new entry
     """
    form = SummaryForm()
    saved_data = read_js(data_path)["data"]

    # Validate incoming form data
    if form.validate_on_submit():
        saved_data.append({
            "summary": form.summary.data,
            "created_at": time.time(),
            "id": str(uuid.uuid4()),
        })

        save_data(saved_data, data_path, key)
        return redirect(url_for('.index'))

    if form.errors:
        print(form.errors)

    # Display standard page
    return render_template(
        'summary/index.html',
        data=sorted(saved_data, key=lambda k: k['created_at'], reverse=True),
        form=form,
        title='Summary Manager'
    )


@summary_bp.route('/update-github', methods=['GET'])
def update_github():
    """
     GET: Pushes saved data to github using GitHub API
     """
    response = update_file(data_path, github_path)
    print(response)
    print(response.content)

    return redirect(url_for('.index'))


@summary_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    """
     GET: Display entry data in form
     POST: Updates entry
     """
    form = SummaryForm()
    saved_data = read_js(data_path)["data"]
    entry_to_edit = get_object_by_id(saved_data, id)

    # Validate incoming form data
    if form.validate_on_submit():
        # Remove old item
        saved_data.remove(entry_to_edit)
        # Add updated item
        saved_data.append({
            "summary": form.summary.data,
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
    form.summary.data = entry_to_edit.get('summary', '')

    return render_template(
        'summary/edit.html',
        data=entry_to_edit,
        form=form,
        title='Edit Summary Entry'
    )


@summary_bp.route('/delete/<id>', methods=['GET'])
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

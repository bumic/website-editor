import time
import uuid
from flask import Blueprint, render_template, request, redirect, url_for
from .forms import PaperForm
from ...utils import read_js, save_data, get_object_by_id
from ...github_utils import update_file


papers_bp = Blueprint('papers', __name__, url_prefix='/papers')
data_path = 'app/data/papers.js'
key = 'papers'
github_path = 'https://api.github.com/repos/ddehueck/ddehueck.github.io/contents/data/papers.js'


@papers_bp.route('/', methods=['GET', 'POST'])
def index():
    """
     GET: Display papers and form
     POST: Creates new paper entry
     """
    form = PaperForm()
    saved_paper_data = read_js(data_path)["data"]

    # Validate incoming form data
    if form.validate_on_submit():
        saved_paper_data.append({
            "citation": form.citation.data,
            "link": form.link.data,
            "notes": form.notes.data,
            "created_at": time.time(),
            "id": str(uuid.uuid4()),
        })

        save_data(saved_paper_data, data_path, key)
        return redirect(url_for('.index'))

    if form.errors:
        print(form.errors)

    # Display standard page
    return render_template(
        'papers/index.html',
        data=sorted(saved_paper_data, key=lambda k: k['created_at'], reverse=True),
        form=form,
        title='Papers Manager'
    )


@papers_bp.route('/update-github', methods=['GET'])
def update_github():
    """
     GET: Pushes saved data to github using GitHub API
     """
    response = update_file(data_path, github_path)
    print(response)
    print(response.content)

    return redirect(url_for('.index'))


@papers_bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    """
     GET: Display paper data in form
     POST: Updates entry
     """
    form = PaperForm()
    saved_paper_data = read_js(data_path)["data"]
    paper_to_edit = get_object_by_id(saved_paper_data, id)

    # Validate incoming form data
    if form.validate_on_submit():
        # Remove old item
        saved_paper_data.remove(paper_to_edit)
        # Add updated item
        saved_paper_data.append({
            "citation": form.citation.data,
            "link": form.link.data,
            "notes": form.notes.data,
            "last_updated": time.time(),
            # Static fields below
            "created_at": paper_to_edit['created_at'],
            "id": paper_to_edit['id'],
        })

        save_data(saved_paper_data, data_path, key)
        return redirect(url_for('.index'))

    if form.errors:
        print(form.errors)

    # Display form with prefilled data
    form.citation.data = paper_to_edit.get('citation', '')
    form.link.data = paper_to_edit.get('link', '')
    form.notes.data = paper_to_edit.get('notes', '')

    return render_template(
        'papers/edit.html',
        data=paper_to_edit,
        form=form,
        title='Edit Paper Entry'
    )


@papers_bp.route('/delete/<id>', methods=['GET'])
def delete(id):
    """
     GET: Removes paper
     """
    # Select paper
    saved_paper_data = read_js(data_path)["data"]
    paper_to_del = get_object_by_id(saved_paper_data, id)

    # Remove and save!
    saved_paper_data.remove(paper_to_del)
    save_data(saved_paper_data, data_path, key)

    return redirect(url_for('.index'))

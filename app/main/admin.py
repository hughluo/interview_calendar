from flask import render_template, redirect, url_for, request
from app.main import main
from app.models.candidate import Candidate
from app.models.interviewer import Interviewer


# admin enable some gui control of adding candidates and interviewers

@main.route('/admin')
def admin():
    return render_template('admin.html')


@main.route('/admin/candidate', methods=['POST'])
def add_candidate():
    form = request.form
    print('form is', form)
    name = form.get('candidate_name', -1)
    print('name is', name)
    Candidate.new(name=name)
    return redirect(url_for('.admin'))


@main.route('/admin/interviewer', methods=['POST'])
def add_interviewer():
    form = request.form
    print('form is', form)
    name = form.get('interviewer_name', -1)
    print('name is', name)
    Interviewer.new(name=name)
    return redirect(url_for('.admin'))

from flask import g, render_template, request, redirect, abort

from app.spendings import bp
from app.db import get_spending_db


@bp.route('/')
def get_spendings():
    spendings = get_spending_db().get_spendings()
    spendings_dict = []
    for spending in spendings:
        spendings_dict.append({
            "id": spending[0],
            "name": spending[1],
            "category": spending[2],
            "date": spending[3],
            "sum0": spending[4],
            "is_spending": spending[5],
        })
    return render_template('spendings/index.html', spendings=spendings_dict)


@bp.route('/create', methods=['GET', 'POST'])
def create_spending():
    if request.method == 'GET':
        return render_template('spendings/create.html')
    else:
        name = request.form.get('name')
        category = request.form.get('category')
        date = request.form.get('date')
        sum0 = request.form.get('sum0')
        spending_or_salary = request.form.get('spending_or_salary')
        db = get_spending_db()

        db.create_spending(name=name, category_id=category, date=date, spending=sum0, is_spending=spending_or_salary)
        return redirect('/spendings', code=302)


@bp.route('/edit/<int:spending_id>', methods=['GET', 'POST'])
def edit_spending(spending_id):
    db = get_spending_db()
    if request.method == 'GET':
        spending = db.get_spending(id=spending_id)
        if spending:
            print(spending)
            return render_template('spendings/edit.html', name=spending[1], category=spending[2], date=spending[3], sum0=spending[4], spending_or_salary=spending[5])
        abort(404)
    else:
        name = request.form.get('name')
        category = request.form.get('category')
        date = request.form.get('date')
        sum0 = request.form.get('sum')
        spending_or_salary = request.form.get('spending_or_salary')

        db.edit_spending(id=spending_id, name=name, category_id=category, date=date, spending=sum0, is_spending=spending_or_salary)
        return redirect('/spendings', code=302)


@bp.route('/delete/<int:spending_id>', methods=['GET', 'POST'])
def delete_spending(spending_id):
    db = get_spending_db()
    if request.method == 'GET':
        spending = db.get_spending(id=spending_id)
        if spending:
            return render_template('spendings/delete.html', name=spending[0], category=spending[1], date=spending[2], sum0=spending[4], spending_or_salary=spending[5])
        abort(404)
    else:
        db.delete_spending(id=spending_id)
        return redirect('/spendings', code=302)
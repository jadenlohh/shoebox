from flask import Blueprint, render_template
import json

router = Blueprint('support', __name__, template_folder='./templates')


@router.get('/support')
def support():
    return render_template('customer/support.html')


@router.get('/support/retrive')
def get_questions():
    questions = []

    with open('./data/questions.json', 'r') as j:
        data = json.load(j)

        for i in data:
            if i['category'] == 'orders&delivery':
                questions.append(i)

        return json.dumps(questions)


@router.get('/support/<category>')
def support_categories(category):
    return render_template('customer/support.html', category=category)
from django import template

register = template.Library()


@register.inclusion_tag('correct_answer.html', takes_context=True)
def correct_answer_for_all(context, question):
    """
    processes the correct answer based on a given question object
    if the answer is incorrect, informs the user
    """
    answers = question.get_answers()
    incorrect_list = context.get('incorrect_questions', [])
    if question.id in incorrect_list:
        user_was_incorrect = True
    else:
        user_was_incorrect = False
    for ans in answers:
        print(ans.id)
    print(type(question.user_answer))
    print(question.user_answer)
    return {'previous': {'answers': answers},
            'user_was_incorrect': user_was_incorrect, 'guess': int(question.user_answer)}


@register.filter
def answer_choice_to_string(question, answer):
    return question.answer_choice_to_string(answer)


@register.filter
def to_char(value):
    return chr(64 + value)


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)

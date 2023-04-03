from django.forms import RadioSelect, CheckboxSelectMultiple


# class CustomRadioSelect(RadioSelect):
#     template_name = 'custom_radioselect.html'
#

class CustomRadioSelect(RadioSelect):
    template_name = 'c_radio.html'
    option_template_name = 'c_radio_option.html'


class CustomCheckboxSelectMultiple(CheckboxSelectMultiple):
    allow_multiple_selected = True
    input_type = 'checkbox'
    template_name = 'checkbox_select.html'
    option_template_name = 'checkbox_option.html'

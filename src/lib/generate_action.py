from flask import url_for
def generate_action(value=None, redirect_function=None, method="get", col_size='', value_name='id',  **kwargs):
    if col_size:
        col_size = f'-{col_size}'
    if kwargs.get('disabled'):
        button = f"""
            <button method="post" class="{kwargs.get('button_class')}" disabled>
                <i class="{kwargs.get('text_class')}" aria-hidden="true"></i>
            </button>
        """
    else:
        button = f"""
            <button method="post" class="{kwargs.get('button_class')}"
                name="{value_name}" value="{value}" title="{kwargs.get("title")}" 
                formaction="{url_for(redirect_function)}">
                    <i class="{kwargs.get('text_class')}" aria-hidden="true"></i>
            </button>
        """
    hidden = ''
    if kwargs.get('hiddens'):
        for hidden in kwargs.get('hiddens'):
            hidden = f'<input name="{hidden["name"]}" value="{hidden["data"]}" type="hidden">\n'

    return f"""
    <div class="col{col_size}">
        <form method="{method}">
            {hidden}          
            {button}        
        </form>
    </div>
    """
    
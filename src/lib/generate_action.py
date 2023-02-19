from flask import url_for
def generate_action(value=None, redirect_function=None, method="get", col_size='', **kwargs):
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
                name="id" value="{value}" 
                formaction="{url_for(redirect_function)}">
                    <i class="{kwargs.get('text_class')}" aria-hidden="true"></i>
            </button>
        """

    return f"""
    <div class="col{col_size}">
        <form method="{method}">            
            {button}        
        </form>
    </div>
    """
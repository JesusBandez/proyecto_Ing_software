from flask import url_for
def generate_action(value=None, redirect_function=None, method="get", **kwargs):
    
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
    <form class="text-center" method="{method}">
        {button}
    </form>
    """
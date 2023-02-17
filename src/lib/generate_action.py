from flask import url_for
def generate_action(value=None, redirect_function=None,**kwargs):
    if kwargs.get('disabled'):
        return f"""
        <form class="text-center" method="post">
            <button method="post" class="{kwargs.get('button_class')}" disabled>
                <i class="{kwargs.get('text_class')}" aria-hidden="true"></i>
            </button>
        </form>
        """
    
    return f"""
        <form class="text-center" method="post">
            <button method="post" class="{kwargs.get('button_class')}"
                name="id" value="{value}" 
                formaction="{url_for(redirect_function)}">
                    <i class="{kwargs.get('text_class')}" aria-hidden="true"></i>
            </button>
        </form>
        """

from abc import ABC, abstractmethod
from src.lib.generate_action import generate_action
from src.routes.auth import has_role, is_project_manager
from src.models.User import User
from src.models.Measures import Measures

from src.models import db



def generate_button(argument,x):
    output = None
    if "hiddens" in argument.keys() and "value_name" in argument.keys():
        output = generate_action(x,
            argument["name"], button_class=argument["button_class"],
            text_class=argument["text_class"],
            title=argument["title"],
            disabled = argument["disable"],
            method = argument["method"] if "method" in argument.keys() else "get",
            hiddens = argument["hiddens"],
            value_name = argument["value_name"])
    elif "hiddens" in argument.keys():
        output = generate_action(x,
            argument["name"], button_class=argument["button_class"],
            text_class=argument["text_class"],
            title=argument["title"],
            disabled = argument["disable"],
            method = argument["method"] if "method" in argument.keys() else "get",
            hiddens = argument["hiddens"])
    else:
        output = generate_action(x,
            argument["name"], button_class=argument["button_class"],
            text_class=argument["text_class"],
            title=argument["title"],
            disabled = argument["disable"],
            method = argument["method"] if "method" in argument.keys() else "get")
    return output

class ListBody(ABC):
    @abstractmethod
    def __init__(self, lists):
        self.lists = lists
        self.args = []
        self.header = []

    @abstractmethod
    def data(self,x):
        return []

    def list_table(self):
        list_body = []
        for x in self.lists:
            actions = []
            for argument in self.args:
                actions.append(generate_button(argument,x.id))
            data = self.data(x)
            list_body.append({
                    'data' : data,
                    'actions' : actions
                    })
        return list_body



class ListProjects(ListBody):
    #projects_list
    def __init__(self, lists):
        self.lists = lists
        self.args = [
            {"button_class":'btn bt-sm btn-outline-primary', "text_class" : 'fa-regular fa-rectangle-list',
            "title":"Project Details", "name":'generate_project', "disable":False},
            {"button_class":'btn bt-sm btn-outline-danger', "text_class" : 'fa-solid fa-trash',
            "title":"Remove project", "name":'remove_project', "disable":not has_role('admin') and not has_role('mngr')},
            {"button_class":'btn bt-sm btn-outline-success', "text_class" : 'fa-solid fa-sack-dollar',
            "title":"Project Budget", "name":'project_budget',"disable":not has_role('admin') and not has_role('mngr')}
        ]
        self.header = [
            {'label': 'Id', 'class': 'col'},
            {'label': 'Car', 'class': 'col'},
            {'label': 'Department', 'class': 'col'},
            {'label': 'Manager', 'class': 'col'},
            {'label': 'Issue', 'class': 'col'},
            {'label': 'Solution', 'class': 'col'}, 
            {'label': 'Amount ($)', 'class': 'col'},
            {'label': 'Observations', 'class': 'col'},            
            {'label': 'Actions', 'class': 'col'},        
        ]

    def data(self,x):
        if x.manager:
            manager_name = x.manager.first_name +" "+ x.manager.last_name
        else:
            manager_name = 'Without manager'       
        
        car_plate = x.car if x.car else 'N/A'
        
        department_description = (
            x.associated_department.description if x.associated_department else 'N/A')
        return [x.id, car_plate, department_description, manager_name, x.issue, x.solution, f'{x.project_cost()}$', x.observations]


class ListProjectsUser(ListBody):
    #project_details
    def __init__(self, lists):
        self.lists = lists
        self.args = [
            {"button_class":'btn btn-outline-primary', "text_class" : 'fa-solid fa-eye',
            "title":"View user details", "name":'user_details', "disable":False}
        ]
        self.header = [
            {'label': 'Id', 'class': 'col-1'},
            {'label': 'First name', 'class': 'col-3'},
            {'label': 'Last name', 'class': 'col-3'},
            {'label' : 'Job', 'class' : 'col-3'},
            {'label' : 'Actions', 'class': 'col-1'} 
        ]

    def data(self,x):
        return [x.id, x.first_name, x.last_name, x.job]


class ListManageProjectUsers(ListBody):
    #manage_project
    def __init__(self, lists,mode,pid):
        self.lists = lists
        self.mode = mode
        self.args = []
        self.project = pid
        self.header = [
            {'label': 'Id', 'class': 'col-1'},
            {'label': 'First name', 'class': 'col-6'},
            {'label': 'Last name', 'class': 'col-2'},
            {'label' : 'actions', 'class': 'col-1'} 
        ]

    def button_to_create(self):
        input_hidden = [{'name' : 'project_id', 'data' : self.project.id}]        
        
        if self.mode == "Add":
            self.args = [{"button_class":'btn btn-outline-primary', "text_class" : 'fa-solid fa-plus',
            "title":"Add user", "name":'add_user_to_project', "disable": (not is_project_manager(self.project)
                and not has_role('admin') and not has_role('mngr')), 
            "method" : 'post', "hiddens" : input_hidden}]
        else:
            self.args = [{"button_class":'btn btn-outline-danger', "text_class" : 'fa fa-trash',
            "title":"Remove user", "name":'remove_user_from_project', "disable":(not is_project_manager(self.project)
                and not has_role('admin') and not has_role('mngr')),
            "method" : 'post', "hiddens" : input_hidden}]

    def data(self,x):
        return [x.id, x.first_name, x.last_name]


class ListUsersList(ListBody):
    #users_lists
    def __init__(self, lists):
        self.lists = lists
        self.args = [
            {"button_class":'btn btn-outline-danger', "text_class" : 'fa fa-trash',
            "title":"Delete user", "name":'delete_user', "method":"post", "disable":not has_role('admin')},
            {"button_class":'btn btn-outline-primary', "text_class" : 'fa-solid fa-eye',
            "title":"View the projects associated with the user", "name":'user_details', "disable":False},
            {"button_class":'btn btn-outline-primary', "text_class" : 'fa-solid fa-pencil',
            "title":"Edit the user", "name":'new_user', "method":"post", "disable": not has_role('admin')}
        ]
        self.header = [
            {'label': 'Id', 'class': 'col-1'},
            {'label': 'Login', 'class': 'col-2'},
            {'label': 'First name', 'class': 'col-2'},
            {'label': 'Last name', 'class': 'col-2'},
            {'label': 'Role', 'class': 'col-2'},
            {'label': 'Actions', 'class': 'col-2'}
        ]

    def data(self,x):
        return [x.id, x.username, x.first_name, x.last_name, x.job]

class ListProjectsOfUser(ListBody):
    #user_details
    def __init__(self, lists,user):
        self.lists = lists
        self.user = user
        self.args = [
            {"button_class":'btn btn-outline-primary', "text_class" : 'fa-solid fa-eye',
            "title":"View project details", "name":'project_details', "disable":False}
        ]
        self.header = [
            {'label': 'Id', 'class': 'col-1'},
            {'label': 'Description', 'class': 'col-6'},
            {'label': 'Start', 'class': 'col-2'},
            {'label': 'End', 'class': 'col-2'},
            {'label' : 'actions', 'class': 'col-1'} 
        ]

    def data(self,p):
        return [p.id, p.description, p.start.strftime(f'%m-%d-%Y'), p.finish.strftime(f'%m-%d-%Y')]

    def list_table(self):
        list_body = []
        for p in self.lists:
            for u in p.users:
                actions = []
                for argument in self.args:
                    actions.append(generate_action(p.id,
                        argument["name"], button_class=argument["button_class"],
                        text_class=argument["text_class"],
                        title=argument["title"],
                        disabled = argument["disable"],
                        method = argument["method"] if "method" in argument.keys() else "get"))
                if (u.id == self.user.id):
                    list_body.append({
                        'data' : self.data(p),
                        'actions' : actions
                    })
        return list_body

class ListEvents(ListBody):
    #logger
    def __init__(self, lists):
        self.lists = lists
        self.args = [
            {"button_class":'btn btn-sm btn-outline-danger w-100', "text_class" : 'fa-solid fa-trash',
            "title":"Remove event", "name":'remove_event', "method" : "post","disable":False},
            {"button_class":'btn btn-sm btn-outline-primary w-100', "text_class" : 'fa-solid fa-table-list',
            "title":"Foo event", "name":'foo_event',"disable":False}
        ]
        self.header = [
            {'label': 'Id', 'class': 'col-1'},
            {'label': 'Event', 'class': 'col-3'},
            {'label': 'Date', 'class': 'col-2'},
            {'label': 'Hour', 'class': 'col-1'},
            {'label': 'Actions', 'class': 'col-2'},
        ]

    def data(self,x):
        return [x.id, x.event, x.date.strftime(f'%m-%d-%Y'), x.hour.strftime(f'%H:%M:%S')]

class ListDepartments(ListBody):
    #departments
    def __init__(self, lists):
        self.lists = lists
        self.args = [
            {"button_class":'btn btn-sm btn-outline-success', "text_class" : 'fa-solid fa-pencil',
            "title":"Edit department", "name":'new_department', "disable":not has_role('opera')},
            {"button_class":'btn btn-sm btn-outline-danger', "text_class" : 'fa-solid fa-trash',
            "title":"Remove department", "name":'remove_department', "method" : "post", "disable":not has_role('opera')}
        ]
        self.header = [
            {'label': 'Id', 'class': 'col-1'},
            {'label': 'Description', 'class': 'col'},
            {'label': 'Actions', 'class': 'col-2'}, 
        ]

    def data(self,x):
        return [x.id, x.description]

class ListClients(ListBody):
    #clients_list
    def __init__(self, lists):
        self.lists = lists
        self.args = [
            {"button_class":'btn btn-sm btn-outline-primary', "text_class" : 'fa fa-car',
            "title":"See client information", "name":'client_details', "disable":False},
            {"button_class":'btn btn-sm btn-outline-success', "text_class" : 'fa-solid fa-pencil',
            "title":"Edit client", "name":'new_client', "disable":not has_role('opera')},
            {"button_class":'btn btn-sm btn-outline-danger', "text_class" : 'fa-solid fa-trash',
            "title":"Remove client", "name":'remove_client', "method" : "post", "disable":not has_role('opera')}
        ]
        self.header = [
            {'label': 'C.I.', 'class': 'col-1'},
            {'label': 'Name', 'class': 'col-1'},
            {'label': 'Lastname', 'class': 'col-1'},
            {'label': 'Birthdate', 'class': 'col-1'},
            {'label': 'Phone Number', 'class': 'col-2'},
            {'label': 'Mail', 'class': 'col-2'},
            {'label': 'Address', 'class': 'col-2'},
            {'label': 'Actions', 'class': 'col-2'}, 
        ]


    def data(self,x):
        return [x.ci, x.first_name, x.last_name, x.birth_date.strftime(f'%m-%d-%Y'), x.phone, x.mail, x.address]
         

class ListClientsCars(ListBody):
    #client_details
    def __init__(self, lists,cid):
        self.lists = lists
        self.client_id = cid
        self.args = [
            {"button_class":'btn btn-sm btn-outline-danger', "text_class" : 'fa-solid fa-trash',
            "title":"Remove car", "name":'remove_car', "method" : "post" ,"disable":not has_role('opera'),
            "hiddens" : [{'name' : 'owner_id', 'data': self.client_id}]},
            {"button_class":'btn btn-sm btn-outline-success', "text_class" : 'fa-solid fa-pencil',
            "title":"Edit car", "name":'new_car', "disable":not has_role('opera'),
            "hiddens" : [{'name' : 'id', 'data': self.client_id}] , "value_name" : 'car_plate'}
        ]
        self.header = [
            {'label': 'License Plate', 'class': 'col-1'},
            {'label': 'Brand', 'class': 'col-2'},
            {'label': 'Model', 'class': 'col-1'},
            {'label': 'Color', 'class': 'col-1'},
            {'label': 'Issue', 'class': 'col-5'},
            {'label': 'Actions', 'class': 'col-1'}
        ]        

    def data(self,x):
        return [x.license_plate, x.brand, x.model, x.color.capitalize(), x.issue]

    def list_table(self):
        list_body = []
        for x in self.lists:
            actions = []
            for argument in self.args:
                actions.append(generate_button(argument,x.license_plate))
            data = self.data(x)
            list_body.append({
                    'data' : data,
                    'actions' : actions
                    })
        return list_body
    
class ListMeasuresList(ListBody):
    #measures_lists
    def __init__(self, lists):
        self.lists = lists
        self.args = [
            {"button_class":'btn btn-outline-danger', "text_class" : 'fa fa-trash',
            "title":"Delete measure", "name":'delete_measure', "method":"post", "disable":not has_role('admin')},
            {"button_class":'btn btn-outline-primary', "text_class" : 'fa-solid fa-pencil',
            "title":"Edit the measure", "name":'new_measure', "method":"post", "disable": not has_role('admin')}
        ]
        self.header = [
            {'label': 'Id', 'class': 'col-1'},
            {'label': 'Dimension', 'class': 'col-2'},
            {'label': 'Unit', 'class': 'col-2'},
            {'label': 'Actions', 'class': 'col-2'}
        ]

    def data(self,x):
        return [x.id, x.dimension, x.unit]
    
class ListActionPlansList(ListBody):
    #action_plans_lists
    def __init__(self, lists, project_id):
        self.lists = lists
        self.args = [
            {"button_class":'btn btn-outline-danger', "text_class" : 'fa fa-trash',
            "title":"Delete action plan", "name":'delete_action_plan', "method":"post", "disable":not has_role('admin'), 
            "hiddens" : [{'name' : 'project_id', 'data' : project_id}]},
            {"button_class":'btn btn-outline-primary', "text_class" : 'fa-solid fa-pencil',
            "title":"Edit the action_plan", "name":'new_action_plan', "method":"post", "disable": not has_role('admin'),
            },
            {"button_class":'btn btn-outline-primary', "text_class" : 'fa-solid fa-eye', "method" : 'get',
            "title":"View plan details", "name":'action_plan_details', "disable": False,
            "hiddens" : [{'name' : 'project_id', 'data' : project_id}]}
        ]
        self.header = [
            {'label': 'Id', 'class': 'col-1'},
            {'label': 'Action', 'class': 'col-2'},
            {'label': 'Activity', 'class': 'col-2'},
            {'label': 'Responsible', 'class': 'col-1'},
            {'label': 'Cost', 'class': 'col-1'},
            {'label': 'Actions', 'class': 'col-1'}
        ]

    def data(self,x):
        r = db.session.query(User).filter(User.id == x.responsible).first()
            
        return [x.id, x.action, x.activity, r.first_name + " " + r.last_name, 
            f'{x.plan_cost()}$']

class ListHumanTalents(ListBody):
    #Human talents
    def __init__(self, lists, project_id, plan_id):
        self.lists = lists
        self.args = [
            {"button_class":'btn btn-outline-danger', "text_class" : 'fa fa-trash',
            "title":"Delete Human Talent", "name":'remove_human_talent', "method":"post", "disable":not has_role('admin'), 
            "hiddens" : [{'name' : 'project_id', 'data' : project_id}, {'name' : 'plan_id', 'data' : plan_id}]},
            {"button_class":'btn btn-outline-primary', "text_class" : 'fa-solid fa-pencil',
            "title":"Edit Human Talent", "name":'new_human_talent', "method":"get", "disable": not has_role('admin'),
            "hiddens" : [{'name' : 'project_id', 'data' : project_id}, {'name' : 'plan_id', 'data' : plan_id}]},
        ]
        self.header = [
            {'label': 'Id', 'class': 'col-1'},
            {'label': 'Action', 'class': 'col-2'},
            {'label': 'Activity', 'class': 'col-2'},            
            {'label': 'Time', 'class': 'col-1'},
            {'label': 'Quantity', 'class': 'col-1'},
            {'label': 'Responsible', 'class': 'col-1'},
            {'label': 'Amount', 'class': 'col-1'},
            {'label': 'Actions', 'class': 'col-1'}
        ]

    def data(self,x):
        r = db.session.query(User).filter(User.id == x.responsible).first()
        return [x.id, x.action, x.activity, x.time, x.quantity, r.first_name + " " + r.last_name, f'{x.total_amount()}$']

class ListMaterialSupplies(ListBody):
    #Material Supplies talents
    def __init__(self, lists, project_id, plan_id):
        self.lists = lists
        self.args = [
            {"button_class":'btn btn-outline-danger', "text_class" : 'fa fa-trash',
            "title":"Delete Supply", "name":'remove_supply', "method":"post", "disable":not has_role('admin'), 
            "hiddens" : [{'name' : 'project_id', 'data' : project_id}, {'name' : 'plan_id', 'data' : plan_id}]},
            {"button_class":'btn btn-outline-primary', "text_class" : 'fa-solid fa-pencil',
            "title":"Edit Supply", "name":'new_supply', "method":"get", "disable": not has_role('admin'),
            "hiddens" : [{'name' : 'project_id', 'data' : project_id}, {'name' : 'plan_id', 'data' : plan_id}]},
        ]
        self.header = [
            {'label': 'Id', 'class': 'col-1'},
            {'label': 'Action', 'class': 'col-2'},
            {'label': 'Activity', 'class': 'col-2'},            
            {'label': 'Category', 'class': 'col-1'},
            {'label': 'Description', 'class': 'col-1'},
            {'label': 'Quantity', 'class': 'col-1'},
            {'label': 'Measure Unit', 'class': 'col-1'},
            {'label': 'Responsible', 'class': 'col-1'},
            {'label': 'Amount', 'class': 'col-1'},
            {'label': 'Actions', 'class': 'col-1'}
        ]

    def data(self,x):
        r = db.session.query(User).filter(User.id == x.responsible).first()
        unit = db.session.query(Measures).filter(Measures.id == x.measure).first()
        return [x.id, x.action, x.activity, x.category, x.description, x.quantity, unit ,r.first_name + " " + r.last_name, f'{x.total_amount()}$']

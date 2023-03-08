ERROR_MUST_BE_ADMIN = 0
ERROR_MUST_BE_ADMIN_AND_MANAGER = 1
ERROR_MUST_BE_ADMIN_NEW_USER = 2
ERROR_MUST_BE_ADMIN_DELETE_USER = 3
ERROR_USERNAME_ALREADY_USED = 4
ERROR_USERNAME_DONT_EXIST = 5
ERROR_INCORRECT_PASSWORD = 6
ERROR_MUST_BE_ADMIN_ADD_CLIENT = 7
ERROR_MUST_BE_ADMIN_DELETE_CLIENT = 8
ERROR_EXISTS_LICENSE_PLATE = 9
ERROR_CI_ALREADY_EXISTS = 10

class Errors(): 
    def __init__(self,number):
        self.error = ErrorType(number)
 
    def show(self):
        print ('Type:', self.name)
 
  
class ErrorType:
 
    def __init__(self,number):
        self.title = self.title(number)
        self.description = self.description(number)
 
    def title(self,n):
        return "ERROR => Nombre del error Modificar en errors.py"
    def description(self,n):
        if n==ERROR_MUST_BE_ADMIN:
            return "Para acceder a esta opcion debes ser admin."
        elif n==ERROR_MUST_BE_ADMIN_AND_MANAGER:
            return "Para acceder debes ser administrador y manager del proyecto"
        elif n==ERROR_MUST_BE_ADMIN_NEW_USER:
            return "Para crear un usuario debes ser administrador"
        elif n==ERROR_MUST_BE_ADMIN_DELETE_USER:
            return "Para eliminar un usuario debes ser administrador"
        elif n==ERROR_USERNAME_ALREADY_USED:
            return "El nombre de usuario ya ha sido utilizado"
        elif n==ERROR_USERNAME_DONT_EXIST:
            return "El nombre de usuario no existe"
        elif n==ERROR_INCORRECT_PASSWORD:
            return "La contrasena es incorrecta"
        elif n==ERROR_MUST_BE_ADMIN_ADD_CLIENT:
            return "Debe ser admin para agregar un cliente"
        elif n==ERROR_MUST_BE_ADMIN_DELETE_CLIENT:
            return "Debe ser admin para eliminar un cliente"
        elif n==ERROR_EXISTS_LICENSE_PLATE:
            return "La placa introducida ya existe"
        elif n==ERROR_CI_ALREADY_EXISTS:
            return "La cedula introducida ya esta registrada"
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
        if n==ERROR_MUST_BE_ADMIN:
            return "ERROR: You're not an administrator"
        elif n==ERROR_MUST_BE_ADMIN_AND_MANAGER:
            return "ERROR: You're not an administrator and manager of this project"
        elif n==ERROR_MUST_BE_ADMIN_NEW_USER:
            return "ERROR: Cannot create new user"
        elif n==ERROR_MUST_BE_ADMIN_DELETE_USER:
            return "ERROR: Cannot delete user"
        elif n==ERROR_USERNAME_ALREADY_USED:
            return "ERROR: The username is in use"
        elif n==ERROR_USERNAME_DONT_EXIST:
            return "ERROR: The username doesn't exist"
        elif n==ERROR_INCORRECT_PASSWORD:
            return "ERROR: Incorrect password"
        elif n==ERROR_MUST_BE_ADMIN_ADD_CLIENT:
            return "ERROR: Cannot add client"
        elif n==ERROR_MUST_BE_ADMIN_DELETE_CLIENT:
            return "ERROR: Cannot delete client"
        elif n==ERROR_EXISTS_LICENSE_PLATE:
            return "ERROR: License plate already exists"
        elif n==ERROR_CI_ALREADY_EXISTS:
            return "ERROR: C.I. already exists"
    def description(self,n):
        if n==ERROR_MUST_BE_ADMIN:
            return "To access this option you must be an administrator."
        elif n==ERROR_MUST_BE_ADMIN_AND_MANAGER:
            return "To access this option you must be an administrator of the system and manager of the project you're trying to access."
        elif n==ERROR_MUST_BE_ADMIN_NEW_USER:
            return "To create a user you must be an administrator."
        elif n==ERROR_MUST_BE_ADMIN_DELETE_USER:
            return "To delete a user you must be an administrator."
        elif n==ERROR_USERNAME_ALREADY_USED:
            return "The username is already taken."
        elif n==ERROR_USERNAME_DONT_EXIST:
            return "The entered username doesn't exist."
        elif n==ERROR_INCORRECT_PASSWORD:
            return "The entered password is incorrect."
        elif n==ERROR_MUST_BE_ADMIN_ADD_CLIENT:
            return "You have to be an administrator to add a client."
        elif n==ERROR_MUST_BE_ADMIN_DELETE_CLIENT:
            return "You have to be an administrator to delete a client."
        elif n==ERROR_EXISTS_LICENSE_PLATE:
            return "The license plate that has been introduced already belongs to an existing car in the system."
        elif n==ERROR_CI_ALREADY_EXISTS:
            return "The introduced C.I. already belongs to a client."
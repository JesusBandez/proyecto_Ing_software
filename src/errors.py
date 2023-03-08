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
    	if n==0:
    		return "Debes ser un administrador"
    def description(self,n):
    	if n==0:
    		return "Para acceder a esta opcion debes ser admin."



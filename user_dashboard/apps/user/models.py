from django.db import models
import bcrypt
# Create your models here.

class PersonManager(models.Manager):
    
    def login(self, form_data):
        errors = []
        try:
            # Check to see if the user exists
            user = Person.objects.get(email = form_data['email'])

            # If user exists then check to see if the password is valid
            if bcrypt.checkpw(form_data['password'].encode(), user.password.encode()):
                print("Inside the successful password check")
                return {'result': 'success', 'user': user}

            # If the password is invalid, send error message
            else:
                errors.append('Login/Password does not match')
                print("Inside the unsuccesful password check ")
                return {'result': 'fail', 'errors': errors}

        except:
            # If the user does not exists send an error message
            errors.append('User witht that email does not exist. Please register.')
            return {'result': 'fail', 'errors': errors}


    def register(self, form_data):
        # index.html => main urls.py => app urls.py => views.py => views.register method => PersonManager.register
        # create a list that holds any error messages
        errors = []

        # Ensure first name exists/length
        if len(form_data['first_name']) < 3:
            errors.append("First name must be at least 2 characters")

        # Ensure last name exists/length
        if len(form_data['last_name']) < 3:
            errors.append("Last name must be at least 2 characters")

        # Ensure email exists/length
        if len(form_data['email']) < 3:
            errors.append("Email must be at least 2 characters")

        # Ensure password exists/length
        if len(form_data['password']) < 8:
            errors.append("Password must be at least 8 characters")

        # Password and password confirmation match
        if not form_data['password'] == form_data['password_confirmation']:
            errors.append("Passwords did not match")

        # Make sure user does not already exist
        try:
            user = Person.objects.get(email = form_data['email'])
            errors.append("Email already in use. Please login")
        except:
            pass
        
        # Check to see if any errors were fired
        if errors:
            return {'errors': errors}
        else:
            person = Person.objects.create(first_name = form_data['first_name'], last_name = form_data['last_name'], email = form_data['email'], password = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt()))
            return {'success': person}
        
class Person(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 255)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    # messages_sent
    # messages_received

    objects = PersonManager()

    def __repr__(self):
        return "<User Object: {} {}>".format(self.first_name, self.last_name)
        # return f "<User Object: {self.first_name} {self.last_name}"

class MessageManager(models.Manager):

    def post_message(self, form_data, receiver_id, sender_id):
        errors = [] 
        if len(form_data['content']) < 10:
            errors.append("You need to love a longer message")
        
        if errors:
            return {'errors': errors}
        else:
            message = Message.objects.create(content = form_data['content'],\
                                            sender = Person.objects.get(id = sender_id), \
                                            receiver = Person.objects.get(id = receiver_id))

            return {'success': message}

class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(Person, related_name='messages_sent')
    receiver = models.ForeignKey(Person, related_name='messages_received')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = MessageManager()

# userOne = Person.objects.get(id = 1)
# userOne.messages_sent.all()
# userOne.messages_received.all()

# messageOne = Message.objects.get(id=1)
# messageOne.sender
# Message.objects.filter(receiver = userOne)

class CommentManager(models.Manager):

    def post_comment(self, form_data, message_id, sender_id):
        errors = [] 
        if len(form_data['content']) < 10:
            errors.append("You need to love a longer message")
        
        if errors:
            return {'errors': errors}
        else:
            comment = Comment.objects.create(content = form_data['content'], \
                                                sender = Person.objects.get(id = sender_id), \
                                                message = Message.objects.get(id = message_id))

            return {'success': comment}


class Comment(models.Model):
    content = models.CharField(max_length = 255)
    message = models.ForeignKey(Message, related_name='comments')
    sender  = models.ForeignKey(Person, related_name='comments_sent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = CommentManager()
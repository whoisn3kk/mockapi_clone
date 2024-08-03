from django.db import models
import bcrypt
import uuid
import json

# Create your models here.


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, '{self.get_repr_key()}')>"

    def get_repr_key(self):
        raise NotImplementedError(
            "Subclasses must implement get_repr_key method")


class Users(BaseModel):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255, default=uuid.uuid4, unique=True)

    def password_check(self, password: str):
        try:
            return bcrypt.checkpw(password.encode(), self.password.encode())
        except:
            return False

    def new_password(self, password: str, any=False):
        if self.password is None or any:
            self.password = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()).decode()
            self.save()
            return True
        return False

    def password_change(self, oldpwd, newpwd):
        if self.password_check(oldpwd):
            return self.new_password(newpwd, True)
        return False
    
    def get_repr_key(self):
        return self.username


class Endpoint(BaseModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.JSONField(default=dict)

    def get_repr_key(self):
        return self.key

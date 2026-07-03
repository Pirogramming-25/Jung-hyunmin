from django.db import models
from devtools.models import DevTool
# Create your models here.
class Idea(models.Model):
  DEVTOOL_CHOICES = [
    ('', '--- 개발도구선택 ---'),
  ]
  title = models.CharField(max_length=50)
  image = models.ImageField(upload_to='ideas/', blank=True, null=True)
  content = models.TextField()
  interest = models.IntegerField(default=0)
  devtool = models.ForeignKey(
    DevTool,
    on_delete=models.CASCADE,
    related_name='ideas',
  )
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return f"{self.title} : {self.content}, {self.interest}, {self.devtool}"

class IdeaStar(models.Model):
  idea = models.OneToOneField(
    Idea,
    on_delete=models.CASCADE,
    related_name='star'
  )
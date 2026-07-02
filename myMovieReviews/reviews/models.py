from django.db import models



# Create your models here.
class Review(models.Model):
  GENRE_CHOICES = [
    ('', '--- 장르선택 ---'),
    ('ACTION', '액션'),
    ('ROMANCE', '로맨스'),
    ('COMEDY', '코미디'),
    ('THRILLER', '스릴러'),
    ('SF', 'SF'),
    ('DRAMA', '드라마')
  ]
  
  title = models.CharField(max_length=50)
  releaseYear = models.IntegerField()
  genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='')
  rating = models.FloatField()
  runningTime = models.IntegerField()
  content = models.CharField(max_length = 500)
  director = models.CharField(max_length = 20)
  mainActor = models.CharField(max_length = 20)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"[{self.genre}] {self.title} -{self.rating}점"
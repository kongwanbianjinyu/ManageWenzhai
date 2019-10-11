
from django.db import models

# Create your models here.
class Book(models.Model):
    BookNumber = models.CharField(max_length=10)# 书籍编号
    BookName = models.CharField(max_length=100) # 书籍标题
    Create_time = models.DateTimeField(auto_now=True) # 创建时间（自动获取当前时间）

    def __str__(self):
        return self.BookNumber

class Label(models.Model):
    Book = models.ForeignKey(Book)#外键关联，指明当前代属于那一本书
    LabelName = models.CharField(max_length=100)
    AllGenerationNum = models.IntegerField() # 总代数限制，真实需要创建的代条数
    ShowGenerationNum = models.FloatField() #对外呈现的代数
    PrintNum = models.IntegerField()  # 每个label的总印数
    Create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

    class Meta:
        unique_together = ("Book", "LabelName")
    def __str__(self):
        return self.LabelName

class Generation(models.Model):
    Label = models.ForeignKey(Label)#外键关联，指明当前代属于那一代
    GenerationNumber = models.CharField(max_length=2)#哪一代
    Contain = models.FloatField() #记录当前代是全代还是半代还是0.25代
    Status = models.CharField(max_length=5) # 印刷状态,'0','1','2'
    Sign = models.CharField(max_length=50)# 印刷人员签名
    AlreadyPrintNum = models.CharField(max_length=50) #已经印刷完的印数
    RemainPrintNum = models.CharField(max_length=50)#剩余印数
    Create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

    class Meta:
        unique_together = ("Label", "GenerationNumber")

    def __str__(self):
        return self.GenerationNumber

from django import forms
from Wenzhai.models import Book,Generation,Label


class SearchBookForm(forms.Form):
    book_name = forms.ModelChoiceField(queryset=Book.objects.all(),label='书籍编号')


class ReviseGenerationForm(forms.Form):
    theBook = forms.ModelChoiceField(queryset=Book.objects.all(),label='书籍编号')#forms.IntegerField(label='书籍编号')
    theLabel = forms.ModelChoiceField(queryset=Label.objects.all(),label='内容标签')
    theGenerationNum = forms.IntegerField(label='所印代数')#forms.ModelChoiceField(label='所印代数',required=True,queryset=Generation.objects.all())#forms.ChoiceField(label='代数',required=True,widget=forms.Select)
    thePrintNum = forms.IntegerField(label='印刷数量')
    #theStatus = forms.BooleanField(label='确认',required=True)
    #theSign = forms.CharField(max_length=5,label='在此签名')
    #part = forms.ModelChoiceField(queryset=Generation.objects.filter(book = Book.objects.filter(BookNumber = '1127')[0]))

class AddBookForm(forms.Form):
    theBookNumber = forms.IntegerField(label='书籍编号')
    theName = forms.CharField(max_length=100,label='书籍名称')
    theLabel = forms.CharField(max_length=100,label='添加标签')
    theAllGenerationNum = forms.FloatField(label='总的代数') #在表单这里填入浮点数，而模型中还是存整型，会在veiws.py中进行转换
    thePrintNum = forms.IntegerField(label='书籍印数')  # 书籍总印数
    
    
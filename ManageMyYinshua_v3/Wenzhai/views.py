
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from Wenzhai.models import Book,Generation,Label
from .forms import SearchBookForm,ReviseGenerationForm,AddBookForm
from datetime import datetime
import math


def index(request):
    return render(request,"index.html")

def login_action(request):
    if (request.method == 'POST'):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            response = HttpResponseRedirect('/search_book_name/')
            request.session['user'] = username
            return response
        else:
            return render(request, 'index.html', {'error': '用户名或密码错误！请重新输入'})

@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response

@login_required
def search_book_name(request):
    # 如果form通过POST方法发送数据
    if request.method == 'POST':
        # 接受request.POST参数构造form类的实例
        form = SearchBookForm(request.POST)
        # 验证数据是否合法
        if form.is_valid():
            book_number = form.cleaned_data['book_name']
            book_list = Book.objects.filter(BookNumber = str(book_number))
            if(book_list):
                mybook =  Book.objects.filter(BookNumber = str(book_number))
                #if(len(mybook)>1):
                    #hint = "致命错误，出现了多个相同编号!! 请立即联系管理员从后台处理"
                    #return render(request, 'event_manage.html', {'form': form,'hint':hint})
                label_list = Label.objects.filter(Book=mybook)
                generation_list = []
                for thisLabel in label_list:
                    generation_list.extend(Generation.objects.filter(Label = thisLabel))
                hint = "查询成功"
            else:
                generation_list = []
                hint = "查询失败，没有相应书籍编号"
            # 处理form.cleaned_data中的数据
            # ...
            # 重定向到一个新的URL
            return render(request, 'event_manage.html', {'form': form,"book_list":book_list,"label_list":label_list,"generation_list":generation_list,'hint':hint})
    else:
        form = SearchBookForm()
    return render(request, 'event_manage.html' ,{'form': form})

@login_required
def add_book(request):
    i = 0
    ActualAllGenerationNum = 0
    generation_list = []
    if request.user.is_superuser:
        if request.method == 'POST':
            form = AddBookForm(request.POST)
            if form.is_valid():
                #收集表单信息
                theBookNumber = form.cleaned_data['theBookNumber']
                theName = form.cleaned_data['theName']
                theLabel = form.cleaned_data['theLabel']
                theAllGenerationNum = form.cleaned_data['theAllGenerationNum']
                thePrintNum = form.cleaned_data['thePrintNum']
                #预处理，先检测一些输入异常
                if(theAllGenerationNum >36 or theAllGenerationNum <=0):
                    hint = "总代数应在1到36之间，请重输"
                    return render(request, 'add_book.html', {'form': form, "hint": hint})
                elif(theAllGenerationNum*4 - math.floor(theAllGenerationNum*4)): #识别是否为.25//.5//.75//.0,只有这几种允许使用
                    hint = "总代数必须是以.0//.25//.5//.75结尾，请重新输入"
                    return render(request, 'add_book.html', {'form': form, "hint": hint})
                else:# 对输入的浮点数进行转换
                    differential = theAllGenerationNum - math.floor(theAllGenerationNum)
                    if(differential == 0.0):
                        ActualAllGenerationNum = int(theAllGenerationNum)
                    elif(differential == 0.25):
                        ActualAllGenerationNum = int(theAllGenerationNum) + 1
                    elif(differential == 0.5):
                        ActualAllGenerationNum = int(theAllGenerationNum) + 1
                    else:
                        ActualAllGenerationNum = int(theAllGenerationNum) + 2

                #找找有没有书
                book_list = Book.objects.filter(BookNumber=str(theBookNumber))
                if(book_list): #有书
                    label_list = Label.objects.filter(Book = book_list[0], LabelName = theLabel)
                    if(label_list):#有书，有标签,禁止
                        hint = "书籍与标签已经存在，请勿重复添加"
                        return render(request, 'add_book.html', {'form': form,"hint":hint})
                    else: #有书，没标签,创建标签和代
                        thisLabel = Label.objects.create(Book = book_list[0],LabelName = theLabel,AllGenerationNum = ActualAllGenerationNum,ShowGenerationNum = theAllGenerationNum,PrintNum = thePrintNum)
                        if (differential == 0.0):  # 整数
                            for i in range(ActualAllGenerationNum):  # 创建和书籍相关联的代数记录
                                generation_list.append(
                                    Generation.objects.create(Label=thisLabel, GenerationNumber=str(i + 1), Contain=1.0,
                                                              Status='未开始', Sign='-', AlreadyPrintNum='0',RemainPrintNum=thePrintNum))
                        elif (differential == 0.25):  # .25代
                            for i in range(ActualAllGenerationNum):  # 创建和书籍相关联的代数记录
                                if (i + 1 == ActualAllGenerationNum - 1):
                                    generation_list.append(
                                        Generation.objects.create(Label=thisLabel, GenerationNumber=str(i + 1),
                                                                  Contain=0.25, Status='未开始', Sign='-',
                                                                  AlreadyPrintNum='0',RemainPrintNum=thePrintNum))
                                else:
                                    generation_list.append(
                                        Generation.objects.create(Label=thisLabel, GenerationNumber=str(i + 1),
                                                                  Contain=1.0, Status='未开始', Sign='-',
                                                                  AlreadyPrintNum='0',RemainPrintNum=thePrintNum))
                        elif (differential == 0.5):
                            for i in range(ActualAllGenerationNum):  # 创建和书籍相关联的代数记录
                                if (i + 1 == ActualAllGenerationNum - 1):
                                    generation_list.append(
                                        Generation.objects.create(Label=thisLabel, GenerationNumber=str(i + 1),
                                                                  Contain=0.5, Status='未开始', Sign='-',
                                                                  AlreadyPrintNum='0',RemainPrintNum=thePrintNum))
                                else:
                                    generation_list.append(
                                        Generation.objects.create(Label=thisLabel, GenerationNumber=str(i + 1),
                                                                  Contain=1.0, Status='未开始', Sign='-',
                                                                  AlreadyPrintNum='0',RemainPrintNum=thePrintNum))
                        else:
                            for i in range(ActualAllGenerationNum):  # 创建和书籍相关联的代数记录
                                if (i + 1 == ActualAllGenerationNum - 2):
                                    generation_list.append(
                                        Generation.objects.create(Label=thisLabel, GenerationNumber=str(i + 1),
                                                                  Contain=0.25, Status='未开始', Sign='-',
                                                                  AlreadyPrintNum='0',RemainPrintNum=thePrintNum))
                                elif (i + 1 == ActualAllGenerationNum - 1):
                                    generation_list.append(
                                        Generation.objects.create(Label=thisLabel, GenerationNumber=str(i + 1),
                                                                  Contain=0.5, Status='未开始', Sign='-',
                                                                  AlreadyPrintNum='0',RemainPrintNum=thePrintNum))
                                else:
                                    generation_list.append(
                                        Generation.objects.create(Label=thisLabel, GenerationNumber=str(i + 1),
                                                                  Contain=1.0, Status='未开始', Sign='-',
                                                                  AlreadyPrintNum='0',RemainPrintNum=thePrintNum))

                        hint = "书籍已存在，已成功创建标签与代"
                        return render(request, 'add_book.html', {'form': form, "hint": hint,"thisBook":book_list[0],"label":thisLabel,"generation_list":generation_list})
                else:#没书
                    #创建书，标签和代
                    thisBook = Book.objects.create(BookNumber = str(theBookNumber),BookName = theName)
                    thisLabel = Label.objects.create(Book = thisBook,LabelName = theLabel,AllGenerationNum = ActualAllGenerationNum,ShowGenerationNum = theAllGenerationNum,PrintNum = thePrintNum)
                    if(differential == 0.0):#整数
                        for i in range(ActualAllGenerationNum):#创建和书籍相关联的代数记录
                            generation_list.append(Generation.objects.create(Label = thisLabel,GenerationNumber = str(i+1),Contain = 1.0,Status= '未开始',Sign = '-', AlreadyPrintNum = '0',RemainPrintNum=thePrintNum))
                    elif(differential == 0.25):#.25代
                        for i in range(ActualAllGenerationNum):#创建和书籍相关联的代数记录
                            if(i+1 == ActualAllGenerationNum-1):
                                generation_list.append(Generation.objects.create(Label = thisLabel,GenerationNumber = str(i+1),Contain = 0.25,Status= '未开始',Sign = '-', AlreadyPrintNum = '0',RemainPrintNum=thePrintNum))
                            else:
                                generation_list.append(Generation.objects.create(Label = thisLabel,GenerationNumber = str(i+1),Contain = 1.0,Status= '未开始',Sign = '-', AlreadyPrintNum = '0',RemainPrintNum=thePrintNum))
                    elif(differential == 0.5):
                        for i in range(ActualAllGenerationNum):#创建和书籍相关联的代数记录
                            if(i+1 == ActualAllGenerationNum-1):
                                generation_list.append(Generation.objects.create(Label = thisLabel,GenerationNumber = str(i+1),Contain = 0.5,Status= '未开始',Sign = '-', AlreadyPrintNum = '0',RemainPrintNum=thePrintNum))
                            else:
                                generation_list.append(Generation.objects.create(Label = thisLabel,GenerationNumber = str(i+1),Contain = 1.0,Status= '未开始',Sign = '-', AlreadyPrintNum = '0',RemainPrintNum=thePrintNum))
                    else:
                        for i in range(ActualAllGenerationNum):#创建和书籍相关联的代数记录
                            if(i+1 == ActualAllGenerationNum-2):
                                generation_list.append(Generation.objects.create(Label = thisLabel,GenerationNumber = str(i+1),Contain = 0.25,Status= '未开始',Sign = '-', AlreadyPrintNum = '0',RemainPrintNum=thePrintNum))
                            elif(i+1 == ActualAllGenerationNum-1):
                                generation_list.append(Generation.objects.create(Label = thisLabel,GenerationNumber = str(i+1),Contain =0.5,Status= '未开始',Sign = '-', AlreadyPrintNum = '0',RemainPrintNum=thePrintNum))
                            else:
                                generation_list.append(Generation.objects.create(Label = thisLabel,GenerationNumber = str(i+1),Contain = 1.0,Status= '未开始',Sign = '-', AlreadyPrintNum = '0',RemainPrintNum=thePrintNum))
                    hint = "书籍、标签与代均已添加成功"
                    return render(request,'add_book.html',{'form':form,"thisBook":thisBook,"label":thisLabel,"generation_list":generation_list,"hint":hint})

        else:
            form =  AddBookForm()
    else:
         return render(request, 'index.html', {'error': '需要超级管理员权限'})
    return render(request, 'add_book.html', {'form': form})


@login_required
def revise_generation(request):

    # 如果form通过POST方法发送数据
    if request.method == 'POST':
        # 接受request.POST参数构造form类的实例
        form = ReviseGenerationForm(request.POST)
        # 验证数据是否合法
        if form.is_valid():
            theBook = form.cleaned_data['theBook']
            theLabel = form.cleaned_data['theLabel']
            theGenerationNum = form.cleaned_data['theGenerationNum']
            thePrintNum = form.cleaned_data['thePrintNum']
            #theSign = form.cleaned_data['theSign']
            theSign = request.session['user']

            thisbook = Book.objects.get(BookNumber=str(theBook))
            label_list = Label.objects.filter(Book = thisbook,LabelName = theLabel)
            
            if(label_list):#有这一个label
                allPrintNum = label_list[0].PrintNum
                generation_list = Generation.objects.filter(Label = label_list[0],GenerationNumber = theGenerationNum)
                if(generation_list):
                    myGeneration  = Generation.objects.get(Label = label_list[0],GenerationNumber = theGenerationNum)
                    previousSign = myGeneration.Sign
                    previousPrintNum = myGeneration.AlreadyPrintNum

                    #进行状态判断，看看是否印完
                    myNumlist = previousPrintNum.split(' | ')
                    SumNum = 0
                    for Num in myNumlist:
                        SumNum = SumNum + int(Num)
                    SumNum = SumNum + thePrintNum

                    if(SumNum >= allPrintNum):
                        changeStatus = '完成'
                        stillRemain = '+' + str(SumNum - allPrintNum)
                    else:
                        changeStatus = '进行中'
                        stillRemain = '-' + str(allPrintNum - SumNum)
                    if(myGeneration.Status == '完成'):
                        hint = "所选代数印刷已完成，请重新选择"
                        return render(request, 'revise_generation.html', {'form': form,"hint":hint})
                    else:
                        Generation.objects.select_for_update().filter(Label = label_list[0],GenerationNumber = theGenerationNum).update(Status = changeStatus,AlreadyPrintNum = previousPrintNum + ' | '+ str(thePrintNum) ,RemainPrintNum = stillRemain, Sign = previousSign + ' | ' + theSign,Create_time = datetime.now())
                        hint = "成功修改"
                        generation_list = Generation.objects.filter(Label=label_list[0],
                                                                    GenerationNumber=theGenerationNum)
                        return render(request, 'revise_generation.html',
                                      {'form': form, "thisbook": thisbook, "generation_list": generation_list,
                                       "hint": hint})
                else:
                    hint = "找不到相应的代，请重新选择"
                    return render(request, 'revise_generation.html', {'form': form, "hint": hint})
            else:
                hint = "找不到相应标签，请重新选择"
                return render(request, 'revise_generation.html',{'form': form,"hint":hint})
    else:
        form = ReviseGenerationForm()
    return render(request, 'revise_generation.html', {'form': form})


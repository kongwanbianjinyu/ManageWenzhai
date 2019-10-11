from django.contrib import admin

# Register your models here.
from Wenzhai.models import Book,Generation,Label
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['BookNumber', 'BookName','Create_time']
class LabelAdmin(admin.ModelAdmin):
    list_display = ['Book', 'LabelName','AllGenerationNum','ShowGenerationNum','PrintNum','Create_time']
class GenerationAdmin(admin.ModelAdmin):
    list_display = ['Label', 'GenerationNumber','Contain','Status','Sign','AlreadyPrintNum','RemainPrintNum','Create_time']
admin.site.register(Book,BookAdmin)
admin.site.register(Label,LabelAdmin)
admin.site.register(Generation,GenerationAdmin)
# Register your models here.

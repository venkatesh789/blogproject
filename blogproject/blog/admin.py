from django.contrib import admin
from blog.models import Post,Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','publish','created','updated','status']
    list_filter=('status','created','publish','author')
    search_fields=('title','body')
    prepopulated_fields={'slug':('title',)}
    raw_id_fields=('author',)
    ordering=['status','publish']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    # list_filter = ('active','created','updated')

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)

from django.contrib import admin

from blogs.models import Blog, Tag


class TagInline(admin.TabularInline):
    model = Blog.tags.through


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug', 'active', 'created_by', 'created_at')
    search_fields = ('title', 'slug')
    list_filter = ('tags', 'created_by', 'created_at')
    readonly_fields = ('created_by', 'updated_by')
    inlines = [TagInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            self.created_by = request.user
        self.updated_by = request.user

        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('name', 'color')
    search_fields = ('name',)
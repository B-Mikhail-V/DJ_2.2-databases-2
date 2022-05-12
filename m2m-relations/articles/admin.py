from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main', False) and not self._should_delete_form(form):
                count += 1
        if count > 1:
            raise ValidationError('Только один тэг может быть основным')
        if count == 0:
            raise ValidationError('Обязательно укажите основной тэг')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]



@admin.register(Tag)
class ArticleAdmin(admin.ModelAdmin):
    pass
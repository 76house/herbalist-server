# coding: utf-8

from datetime import datetime
from django.contrib import admin
from django.forms import ModelForm, MultipleChoiceField, CheckboxSelectMultiple
from django.utils.translation import get_language, ugettext as _
from herbapp.models import Purchase, Author, Disease, Herb, HerbPicture, HerbUsage, HerbPick, ENVIRONMENT_CHOICES


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['order', 'token', 'app_platform', 'app_version', 'app_language', 'screen_width', 'last_sync_ts', 'counter']
    ordering = ['-last_sync_ts']

class AuthorAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.timestamp = datetime.now()
        super(AuthorAdmin, self).save_model(request, obj, form, change)

class DiseaseAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.timestamp = datetime.now()
        super(DiseaseAdmin, self).save_model(request, obj, form, change)


class HerbPickInline(admin.TabularInline):
    model = HerbPick


class HerbUsageInline(admin.TabularInline):
    model = HerbUsage


class HerbForm(ModelForm):
    environment = MultipleChoiceField(choices=ENVIRONMENT_CHOICES, widget=CheckboxSelectMultiple(), required=True, label=_('Environment'))

    class Meta:
        model = Herb

    def clean_csi(self, field): 
        data = self.cleaned_data[field] 
        data.sort() 
        csi_list = [] 
        first_element = True 
        for element in data: 
            if not first_element: 
                csi_list.append(",") 
            else: 
                first_element = False 
            csi_list.append(str(element)) 
        return "".join(csi_list)

    def clean_environment(self): 
        return self.clean_csi('environment')


class HerbAdmin(admin.ModelAdmin):
    form = HerbForm
    list_display = ['name', 'botanical_name', 'family', 'plant_type', 'picture_thumbnails']
    list_filter = ['plant_type']
    ordering = [_('name_en')]
    inlines = [HerbPickInline, HerbUsageInline]
    
    def save_model(self, request, obj, form, change):
        obj.timestamp = datetime.now()
        super(HerbAdmin, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in instances:
            obj.timestamp = datetime.now()
            obj.save()


class HerbPictureAdmin(admin.ModelAdmin):
    list_display = ['herb_id', 'name', 'thumbnail']

    def save_model(self, request, obj, form, change):
        obj.timestamp = datetime.now()
        super(HerbPictureAdmin, self).save_model(request, obj, form, change)


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Herb, HerbAdmin)
admin.site.register(HerbPicture, HerbPictureAdmin)



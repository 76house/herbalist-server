# coding: utf-8

from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms import ModelForm, MultipleChoiceField, CheckboxSelectMultiple
from django.utils.translation import get_language, ugettext as _
from herbapp.models import Purchase, Author, Disease, Herb, HerbPicture, HerbUsage, HerbPick, \
    ENVIRONMENT_CHOICES, AGE_CHOICES, DISEASE_TYPE_CHOICES, BODY_PART_CHOICES, HEAD_PART_CHOICES


# ------------------------------------------------------------------------------

class CsiModelForm(ModelForm):

    # clean the string with a list result of multiple choice widget
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


# ------------------------------------------------------------------------------

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['client_id', 'token', 'app_platform', 'app_version', 'app_language', 'app_region', 'screen_width', 'screen_height', 'last_sync_ts', 'counter']
    ordering = ['-last_sync_ts']


# ------------------------------------------------------------------------------

class AuthorAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.timestamp = datetime.now()
        super(AuthorAdmin, self).save_model(request, obj, form, change)


# ------------------------------------------------------------------------------

class DiseaseForm(CsiModelForm):
    age_group = MultipleChoiceField(choices=AGE_CHOICES, widget=CheckboxSelectMultiple(), required=True, label=_('Age group'))
    disease_type = MultipleChoiceField(choices=DISEASE_TYPE_CHOICES, widget=CheckboxSelectMultiple(), required=True, label=_('Type'))

    body_parts = MultipleChoiceField(choices=BODY_PART_CHOICES, widget=CheckboxSelectMultiple(), required=False, label=_('Body parts'))
    head_parts = MultipleChoiceField(choices=HEAD_PART_CHOICES, widget=CheckboxSelectMultiple(), required=False, label=_('Head parts'))

    class Meta:
        model = Disease

    def clean_age_group(self): 
        return self.clean_csi('age_group')

    def clean_disease_type(self): 
        return self.clean_csi('disease_type')

    def clean_body_parts(self): 
        return self.clean_csi('body_parts')

    def clean_head_parts(self): 
        return self.clean_csi('head_parts')


# ------------------------------------------------------------------------------

class DiseaseAdmin(admin.ModelAdmin):
    form = DiseaseForm
    list_display = [_('name_en'), 'get_disease_type']
    ordering = [_('name_en')]
    search_fields = [_('name_en')]

    def save_model(self, request, obj, form, change):
        obj.timestamp = datetime.now()
        super(DiseaseAdmin, self).save_model(request, obj, form, change)


# ------------------------------------------------------------------------------

# used in Herb
class HerbPickInline(admin.TabularInline):
    model = HerbPick


# ------------------------------------------------------------------------------

# used in Herb
class HerbUsageInline(admin.TabularInline):
    model = HerbUsage


# ------------------------------------------------------------------------------

class HerbForm(CsiModelForm):
    environment = MultipleChoiceField(choices=ENVIRONMENT_CHOICES, widget=CheckboxSelectMultiple(), required=True, label=_('Environment'))

    class Meta:
        model = Herb

    def clean_environment(self): 
        return self.clean_csi('environment')


# ------------------------------------------------------------------------------

class HerbAdmin(admin.ModelAdmin):
    form = HerbForm
    list_display = [_('name_en'), 'botanical_name', 'has_language_en', 'has_language_de', 'has_language_cs', 'plant_type', 'picture_thumbnails']
    list_filter = ['plant_type']
    ordering = [_('name_en')]
    search_fields = [_('name_en')]
    save_on_top = True
    inlines = [HerbPickInline, HerbUsageInline]

    fieldsets = (
        (None, {
            'fields': ('author_id', 'botanical_name', 'is_healing', 'is_toxic', 'plant_type', 'height_min', 'height_max', 'environment')
        }),
        (_('English'), {
            'classes': ('collapse','wide',),
            'fields': ('name_en', 'alias_en', 'description_en')
        }),
        (_('German'), {
            'classes': ('collapse','wide',),
            'fields': ('name_de', 'alias_de', 'description_de')
        }),
        (_('Czech'), {
            'classes': ('collapse','wide',),
            'fields': ('name_cs', 'alias_cs', 'description_cs')
        }),
        (_('Flower'), {
            'fields': ('flower_color', 'flower_type', 'blooming_from', 'blooming_to', 'petal_mincount', 'petal_maxcount')
        }),
        (_('Leaf'), {
            'fields': ('leaf_type', 'leaf_shape', 'leaf_shape_alt', 'leaf_edge', 'leaf_edge_alt', 'leaf_arrangement', 'leaf_arrangement_alt')
        }),
        (_('Shrub / tree'), {
            'fields': ('needle_type', 'branching', 'bark_type', 'bark_type_alt')
        }),
        (_('Fruit'), {
            'fields': ('fruit_type', 'fruit_from', 'fruit_to')
        }),
    )

    class Media:
        # plant-type based field showing
        js = ("/static/js/admin.js",)


    def save_model(self, request, obj, form, change):
        obj.timestamp = datetime.now()
        super(HerbAdmin, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in instances:
            obj.timestamp = datetime.now()
            obj.save()


# ------------------------------------------------------------------------------

class HerbPictureAdmin(admin.ModelAdmin):
    list_display = ['herb_id', 'name', 'thumbnail']

    def save_model(self, request, obj, form, change):
        obj.timestamp = datetime.now()
        super(HerbPictureAdmin, self).save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse("admin:herbapp_herb_changelist"))


# register admins
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Herb, HerbAdmin)
admin.site.register(HerbPicture, HerbPictureAdmin)



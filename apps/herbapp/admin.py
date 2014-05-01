# coding: utf-8

from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms import ModelForm, MultipleChoiceField, CheckboxSelectMultiple
from django.utils.translation import get_language, ugettext as _
from herbapp.models import Purchase, Author, Disease, Herb, HerbPicture, HerbUsage, HerbPick, \
    ENVIRONMENT_CHOICES, AGE_CHOICES, DISEASE_TYPE_CHOICES, BODY_PART_CHOICES, HEAD_PART_CHOICES, \
    EFFECT_SKIN_CHOICES, EFFECT_MUSCULAR_CHOICES, EFFECT_RESPIRATORY_CHOICES, EFFECT_CARDIO_CHOICES, \
    EFFECT_DIGESTIVE_CHOICES, EFFECT_REPRO_CHOICES, EFFECT_INFECTION_CHOICES, \
    REGION_HOLARCTIC_CHOICES, REGION_PALEOTROPICAL_CHOICES, REGION_NEOTROPICAL_CHOICES, \
    REGION_SOUTHAFRICAN_CHOICES, REGION_AUSTRALIAN_CHOICES, REGION_ANTARCTIC_CHOICES


# ------------------------------------------------------------------------------

# Widget for multiple selection
class CSICheckboxSelectMultiple(CheckboxSelectMultiple):
    def value_from_datadict(self, data, files, name):
        # Return a string of comma separated integers since the database, and
        # field expect a string (not a list).
        return ','.join(data.getlist(name))

    def render(self, name, value, attrs=None, choices=()):
        # Convert comma separated integer string to a list, since the checkbox
        # rendering code expects a list (not a string)
        if value:
            value = value.split(',')
        return super(CSICheckboxSelectMultiple, self).render(
            name, value, attrs=attrs, choices=choices
        )


# ------------------------------------------------------------------------------

# Form field for multiple selection
class CSIMultipleChoiceField(MultipleChoiceField):
    widget = CSICheckboxSelectMultiple

    # Value is stored and retrieved as a string of comma separated
    # integers. We don't want to do processing to convert the value to
    # a list like the normal MultipleChoiceField does.
    def to_python(self, value):
        return value

    def validate(self, value):
        # If we have a value, then we know it is a string of comma separated
        # integers. To use the MultipleChoiceField validator, we first have
        # to convert the value to a list.
        if value:
            value = value.split(',')
        super(CSIMultipleChoiceField, self).validate(value)


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

class DiseaseForm(ModelForm):
    age_group = CSIMultipleChoiceField(choices=AGE_CHOICES, widget=CSICheckboxSelectMultiple(), required=True, label=_('Age group'))
    disease_type = CSIMultipleChoiceField(choices=DISEASE_TYPE_CHOICES, widget=CSICheckboxSelectMultiple(), required=True, label=_('Type'))

    body_parts = CSIMultipleChoiceField(choices=BODY_PART_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Body parts'))
    head_parts = CSIMultipleChoiceField(choices=HEAD_PART_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Head parts'))

    class Meta:
        model = Disease


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

class HerbForm(ModelForm):
    environment = CSIMultipleChoiceField(choices=ENVIRONMENT_CHOICES, widget=CSICheckboxSelectMultiple(), required=True, label=_('Environment'))
    effect_skin        = CSIMultipleChoiceField(choices=EFFECT_SKIN_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Skin'))
    effect_muscular    = CSIMultipleChoiceField(choices=EFFECT_MUSCULAR_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Muscular and nervous system'))
    effect_respiratory = CSIMultipleChoiceField(choices=EFFECT_RESPIRATORY_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Respiratory system'))
    effect_cardio      = CSIMultipleChoiceField(choices=EFFECT_CARDIO_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Cardiovascular system'))
    effect_digestive   = CSIMultipleChoiceField(choices=EFFECT_DIGESTIVE_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Digestive and excretory system'))
    effect_repro       = CSIMultipleChoiceField(choices=EFFECT_REPRO_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Reproductive system'))
    effect_infection   = CSIMultipleChoiceField(choices=EFFECT_INFECTION_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Infections'))

    region_holarctic       = CSIMultipleChoiceField(choices=REGION_HOLARCTIC_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Holarctic'))
    region_paleotropical   = CSIMultipleChoiceField(choices=REGION_PALEOTROPICAL_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Paleotropical'))
    region_neotropical     = CSIMultipleChoiceField(choices=REGION_NEOTROPICAL_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Neotropical'))
    region_southafrican    = CSIMultipleChoiceField(choices=REGION_SOUTHAFRICAN_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('South African'))
    region_australian      = CSIMultipleChoiceField(choices=REGION_AUSTRALIAN_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Australian'))
    region_antarctic       = CSIMultipleChoiceField(choices=REGION_ANTARCTIC_CHOICES, widget=CSICheckboxSelectMultiple(), required=False, label=_('Antarctic'))
        
    class Meta:
        model = Herb

    def __init__(self, *args, **kwargs):
        super(HerbForm, self).__init__(*args, **kwargs)
        self.fields['synonyms'].widget.attrs.update({'class' : 'vLargeTextField'})
        self.fields['alias_en'].widget.attrs.update({'class' : 'vLargeTextField'})
        self.fields['alias_de'].widget.attrs.update({'class' : 'vLargeTextField'})
        self.fields['alias_cs'].widget.attrs.update({'class' : 'vLargeTextField'})


# ------------------------------------------------------------------------------

class HerbAdmin(admin.ModelAdmin):
    form = HerbForm
    list_display = ['name_status', 'botanical_name', 'has_language_en', 'has_language_de', 'has_language_cs', 'plant_type', 'picture_thumbnails']
    list_filter = ['plant_type']
    ordering = [_('name_en')]
    search_fields = [_('name_en')]
    save_on_top = True
    inlines = [HerbPickInline, HerbUsageInline]

    fieldsets = (
        (None, {
            'fields': ('is_draft', 'author_id', 'botanical_name', 'synonyms', 'is_healing', 'is_toxic', 'plant_type', 'family', 'height_min', 'height_max', 'environment')
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
        (_('Other languages'), {
            'classes': ('collapse','wide',),
            'fields': ('name_sk', 'name_es', 'name_fr', 'name_it', 'name_ru', 'name_pl', 'name_tr', 'name_ar', 'name_zh')
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
        (_('Distribution'), {
            'classes': ('collapse',),
            'fields': ('region_holarctic', 'region_paleotropical', 'region_neotropical', 'region_southafrican', 'region_australian', 'region_antarctic')
        }),
        (_('Effects'), {
            'classes': ('collapse',),
            'fields': ('effect_skin', 'effect_muscular', 'effect_respiratory', 'effect_cardio', 'effect_digestive', 'effect_repro', 'effect_infection')
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



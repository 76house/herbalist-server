# coding: utf-8

import os
import re
import string
import random
import PIL.ExifTags
from PIL import Image, ImageEnhance
from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import get_language, ugettext_lazy as _


# ------------------------------------------------------------------------------
# Support for DB text localization
#

__all__ = ('Translate', 'LocalizeModelBase')

# a dummy placeholder object
Translate = object()

class LocalizeModelBase(ModelBase):
    """This meta-class provides automatically translated content properties. Set
    a model field to `Translate` and it will automatically return the property
    with the name of the current language. E.g. if there is a normal member
    `text_de`, a member `text = Translate` and the current language is `de`, then
    an object will return the content of `text_de` when it is asked for the value
    of `text`.
    """
    def __new__(metacls, classname, bases, classDict):
        # find all classDict entries that point to `Translate`
        for key in classDict.keys():
            if classDict[key] is Translate:
                # replace them with a getter that uses the current language
                classDict[key] = make_property(key)
        return super(LocalizeModelBase, metacls).__new__(metacls, classname, bases, classDict)


def make_property(k):
    """Creates a new property that implements the automatic translation
    described above. Every use of `Translate` in a class definition will be
    replaced with a property returned by this function."""
    def pget(self):
        try:
            # try to return the attribute for the current language
            return getattr(self, "%s_%s" % (k, get_language()))
        except AttributeError:
            # use the default language if the current language is not available
            return getattr(self, "%s_%s" % (k, settings.LANGUAGE_CODE))
    return property(pget)


# ------------------------------------------------------------------------------
# Purchase model (server only) - used for client authentication via RESTful API
#

class Purchase(models.Model):

    client_id       = models.CharField(max_length=48, verbose_name=_('Client ID'), primary_key=True) # client ID
    token           = models.CharField(max_length=64, verbose_name=_('Token')) # token generated from signature and timestamp
    last_sync_ts    = models.DateTimeField(default=datetime.now, verbose_name=_('Last sync time')) # time of last successful synchronization (seconds)
    app_version     = models.CharField(default='', max_length=16, verbose_name=_('Client version')) # client application: version
    app_platform    = models.CharField(default='', max_length=16, verbose_name=_('Client platform')) # client application: host OS name and version
    app_language    = models.CharField(default='', max_length=2, verbose_name=_('Language')) # client application: language code
    app_region      = models.CharField(default='', max_length=64, verbose_name=_('Region')) # client application: region
    screen_width    = models.IntegerField(default=0, verbose_name=_('Screen width')) # client device: max.screen width
    screen_height   = models.IntegerField(default=0, verbose_name=_('Screen height')) # client device: max.screen height
    counter         = models.IntegerField(default=0, verbose_name=_('Request count')) # how many times the auth request has been called by this client

    class Meta:
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')

    def __unicode__(self):
        return "%s" % self.client_id


# ------------------------------------------------------------------------------
# Author model - DB content editors (herb descriptions, pictures)
#

class Author(models.Model):

    _id             = models.AutoField(primary_key=True)
    name            = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))
    timestamp       = models.DateTimeField(default=datetime.now, editable=False) # last change

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __unicode__(self):
        return "%s" % self.name


# ------------------------------------------------------------------------------
# Disease model - disease list
#

SEX_CHOICES = (
    (1, _('men and women')),
    (2, _('men only')),
    (3, _('women only')),
)

AGE_CHOICES = (
    (1, _('infants')),
    (2, _('children')),
    (3, _('teenagers')),
    (4, _('adults')),
    (5, _('seniors')),
)

DISEASE_TYPE_CHOICES = (
    (1, _('physical')),
    (2, _('psychical')),
)

BODY_PART_CHOICES = (
    (1, _('head / neck')),
    (2, _('skin')),
    (3, _('chest / back')),
    (4, _('stomach / bottom')),
    (5, _('genitourinary tract')),
    (6, _('hands / legs')),
)

HEAD_PART_CHOICES = (
    (1, _('hair')),
    (2, _('brain')),
    (3, _('eyes')),
    (4, _('ears')),
    (5, _('mouth / nose')),
    (6, _('neck')),
)


class Disease(models.Model):
    __metaclass__   = LocalizeModelBase

    _id             = models.AutoField(primary_key=True)
    name_en         = models.CharField(max_length=40, verbose_name=_('Name (EN)'))
    name_de         = models.CharField(max_length=40, verbose_name=_('Name (DE)'))
    name_cs         = models.CharField(max_length=40, verbose_name=_('Name (CS)'))
    name            = Translate
    timestamp       = models.DateTimeField(default=datetime.now, editable=False) # last change
    affected_sex    = models.IntegerField(choices=SEX_CHOICES, default=1, verbose_name=_('Affected sex'))
    age_group       = models.CommaSeparatedIntegerField(max_length=10, default='', verbose_name=_('Age group')) # list of AGE_CHOICES
    disease_type    = models.CommaSeparatedIntegerField(max_length=4, default='1', verbose_name=_('Type')) # list of DISEASE_TYPE_CHOICES
    body_parts      = models.CommaSeparatedIntegerField(max_length=16, null=True, blank=True, default='', verbose_name=_('Body parts')) # list of BODY_PART_CHOICES
    head_parts      = models.CommaSeparatedIntegerField(max_length=14, null=True, blank=True, default='', verbose_name=_('Head parts')) # list of HEAD_PART_CHOICES

    class Meta:
        verbose_name = _('Disease')
        verbose_name_plural = _('Diseases')
        ordering = [_('name_en')]

    def __unicode__(self):
        return "%s" % self.name
        
    def get_disease_type(self):
        names = []
        lst = self.disease_type.split(',')
        for k, v in DISEASE_TYPE_CHOICES:
            if str(k) in lst:
                names.append(''.join(v))
        return ', '.join(names)

    get_disease_type.short_description = _('Type')


# ------------------------------------------------------------------------------
# Herb model - herb descriptions
#

PLANT_CHOICES = (
    (1, _('herb')),
    (2, _('leaf shrub')),
    (3, _('needle shrub')),
    (4, _('leaf tree')),
    (5, _('needle tree')),
)

FLOWER_COLOR_CHOICES = (
    (0, ''),
    (1, _('white')),
    (2, _('yellow')),
    (3, _('brown')),
    (4, _('red / pink')),
    (5, _('blue / magenta')),
    (6, _('green')),
    (7, _('other')),
)

FLOWER_CHOICES = (
    (0, ''),
    (1, _('simple')),
    (2, _('capitulum - disc or ray florets')),
    (3, _('cyme')),
    (4, _('corymb')),
    (5, _('dychasia')),
    (6, _('umbel')),
    (7, _('compound umbel')),
    (8, _('panicle')),
    (9, _('raceme')),
    (10, _('spike')),
    (11, _('head')),
    (12, _('catkin')),
)

MONTH_CHOICES = (
    (0, ''),
    (1, _('january')),
    (2, _('february')),
    (3, _('march')),
    (4, _('april')),
    (5, _('may')),
    (6, _('june')),
    (7, _('july')),
    (8, _('august')),
    (9, _('september')),
    (10, _('october')),
    (11, _('november')),
    (12, _('december')),
)

LEAF_ARRANGEMENT_CHOICES = (
    (0, ''),
    (1, _('alternate')),
    (2, _('opposite')),
    (3, _('verticillate')),
    (4, _('rosette')),
    (5, _('other')),
)

LEAF_EDGE_CHOICES = (
    (0, ''),
    (1, _('entire')),
    (2, _('serrate')),
    (3, _('toothed')),
    (4, _('lobed')),
)

LEAF_CHOICES = (
    (0, ''),
    (1, _('simple unseparated')),
    (2, _('simple hand-shaped')),
    (3, _('simple pinnate')),
    (4, _('compound hand-shaped')),
    (5, _('compound imparipinnate')),
    (6, _('compound paripinnate')),
)

LEAF_SHAPE_CHOICES = (
    (0, ''),
    (1, _('linear')),
    (2, _('circular')),
    (3, _('oval-shaped')),
    (4, _('egg-shaped')),
    (5, _('teardrop-shaped')),
    (6, _('lanceolate')),
    (7, _('wedge-shaped')),
    (8, _('spoon-shaped')),
    (9, _('triangular')),
    (10, _('diamond-shaped')),
    (11, _('heart-shaped')),
    (12, _('inverse heart-shaped')),
    (13, _('kidney-shaped')),
    (14, _('arrow-shaped')),
    (15, _('spear-shaped')),
    (16, _('pinnatisect')),
    (17, _('other')),
)

NEEDLE_CHOICES = (
    (0, ''),
    (1, _('single needles')),
    (2, _('bundled needles')),
    (3, _('tufted needles')),
    (4, _('scales')),
)

BRANCHING_CHOICES = (
    (0, ''),
    (1, _('alternate')),
    (2, _('opposite')),
    (3, _('with thorns')),
)

BARK_CHOICES = (
    (0, ''),
    (1, _('smooth')),
    (2, _('lenticelas')),
    (3, _('grooved')),
    (4, _('scaly')),
)

FRUIT_CHOICES = (
    (0, ''),
    (1, _('legume')),
    (2, _('capsule')),
    (3, _('silique')),
    (4, _('follicle')),
    (5, _('nut / nutlet')),
    (6, _('achene')),
    (7, _('winged achene')),
    (8, _('berries')),
    (9, _('aggregate fruits')),
    (10, _('drupe')),
    (11, _('pome')),
    (12, _('cone')),
)

ENVIRONMENT_CHOICES = (
    (1, _('field')),
    (2, _('grassy')),
    (3, _('forested')),
    (4, _('humid')),
    (5, _('urban')),
    (6, _('mountain')),
)


class Herb(models.Model):
    __metaclass__   = LocalizeModelBase

    _id             = models.AutoField(primary_key=True)
    author_id       = models.ForeignKey('herbapp.Author', default=1, verbose_name=_('Author'))
    timestamp       = models.DateTimeField(default=datetime.now, editable=False) # last change
    botanical_name  = models.CharField(max_length=40, unique=True, verbose_name=_('Latin name'))

    name_en         = models.CharField(max_length=40, verbose_name=_('Common name (EN)'))
    alias_en        = models.CharField(max_length=100, blank=True, verbose_name=_('Folk names (EN)'))
    family_en       = models.CharField(max_length=40, blank=True, verbose_name=_('Family (EN)'))
    description_en  = models.TextField(blank=True, verbose_name=_('Description (EN)'))
    name_de         = models.CharField(max_length=40, verbose_name=_('Common name (DE)'))
    alias_de        = models.CharField(max_length=100, blank=True, verbose_name=_('Folk names (DE)'))
    family_de       = models.CharField(max_length=40, blank=True, verbose_name=_('Family (DE)'))
    description_de  = models.TextField(blank=True, verbose_name=_('Description (DE)'))
    name_cs         = models.CharField(max_length=40, verbose_name=_('Common name (CS)'))
    alias_cs        = models.CharField(max_length=100, blank=True, verbose_name=_('Folk names (CS)'))
    family_cs       = models.CharField(max_length=40, blank=True, verbose_name=_('Family (CS)'))
    description_cs  = models.TextField(blank=True, verbose_name=_('Description (CS)'))

    name            = Translate
    alias           = Translate
    family          = Translate
    description     = Translate

    is_healing      = models.BooleanField(default=True, verbose_name=_('Is healing'))
    is_toxic        = models.BooleanField(default=False, verbose_name=_('Is toxic'))
    plant_type      = models.IntegerField(choices=PLANT_CHOICES, default=1, verbose_name=_('Plant type'))
    height_min      = models.IntegerField(null=True, blank=True, verbose_name=_('Min.height (cm)'))
    height_max      = models.IntegerField(null=True, blank=True, verbose_name=_('Max.height (cm)'))

    flower_color    = models.IntegerField(choices = FLOWER_COLOR_CHOICES, default=0, verbose_name=_('Predominant flower color'))
    flower_type     = models.IntegerField(choices = FLOWER_CHOICES, default=0, verbose_name=_('Flower type'))
    blooming_from   = models.IntegerField(choices = MONTH_CHOICES, default=0, verbose_name=_('Blooming from'))
    blooming_to     = models.IntegerField(choices = MONTH_CHOICES, default=0, verbose_name=_('Blooming to'))
    petal_mincount  = models.IntegerField(null=True, blank=True, verbose_name=_('Min.petal count'))
    petal_maxcount  = models.IntegerField(null=True, blank=True, verbose_name=_('Max.petal count'))
    
    leaf_type       = models.IntegerField(choices = LEAF_CHOICES, default=0, verbose_name=_('Leaf type'))
    leaf_shape      = models.IntegerField(choices = LEAF_SHAPE_CHOICES, default=0, verbose_name=_('Leaf shape'))
    leaf_shape_alt  = models.IntegerField(choices = LEAF_SHAPE_CHOICES, default=0, verbose_name=_('Leaf shape (alt.)'))
    leaf_edge       = models.IntegerField(choices = LEAF_EDGE_CHOICES, default=0, verbose_name=_('Leaf edge'))
    leaf_edge_alt   = models.IntegerField(choices = LEAF_EDGE_CHOICES, default=0, verbose_name=_('Leaf edge (alt.)'))
    leaf_arrangement        = models.IntegerField(choices = LEAF_ARRANGEMENT_CHOICES, default=0, verbose_name=_('Leaf arrangement'))
    leaf_arrangement_alt    = models.IntegerField(choices = LEAF_ARRANGEMENT_CHOICES, default=0, verbose_name=_('Leaf arrangement (alt.)'))

    needle_type     = models.IntegerField(choices = NEEDLE_CHOICES, default=0, verbose_name=_('Needle type'))
    branching       = models.IntegerField(choices = BRANCHING_CHOICES, default=0, verbose_name=_('Ast branching'))
    bark_type       = models.IntegerField(choices = BARK_CHOICES, default=0, verbose_name=_('Bark type'))
    bark_type_alt   = models.IntegerField(choices = BARK_CHOICES, default=0, verbose_name=_('Bark type (alt.)'))

    fruit_type      = models.IntegerField(choices = FRUIT_CHOICES, default=0, verbose_name=_('Fruit type'))
    fruit_from      = models.IntegerField(choices = MONTH_CHOICES, default=0, verbose_name=_('Fruit from'))
    fruit_to        = models.IntegerField(choices = MONTH_CHOICES, default=0, verbose_name=_('Fruit to'))

    environment     = models.CommaSeparatedIntegerField(max_length=15, default='', verbose_name=_('Environment')) # list of ENVIRONMENT_CHOICES

    class Meta:
        verbose_name = _('Herb')
        verbose_name_plural = _('Herbs')
        ordering = [_('name_en')]
        
    def __unicode__(self):
        return "%s" % self.name

    # picture thumbnails in admin list view        
    def picture_thumbnails(self):
        html = ''
        pictures = HerbPicture.objects.filter(herb_id=self._id)
        if pictures.count() > 0:
            for picture in pictures:
                html = html + u'<a href="../herbpicture/%u/"><img style="max-width: 120px; max-height: 120px; " src="%s" /></a> ' \
                    % (picture._id, settings.MEDIA_URL + picture.url(120))
        html = html + (u'<a href="../herbpicture/add/?herb_id=%u">' + u'[+]</a>') % self._id
        return html

    picture_thumbnails.short_description = _('Pictures')
    picture_thumbnails.allow_tags = True

    # displays a bullet if English texts are complete
    def has_language_en(self):
        if (self.name_en != "" and self.alias_en != "" and self.description_en != ""):
            return '<span style="font-size: 16pt;">&bull;</span>'
        else:
            return ""

    # displays a bullet if German texts are complete
    def has_language_de(self):
        if (self.name_de != "" and self.alias_de != "" and self.description_de != ""):
            return '<span style="font-size: 16pt;">&bull;</span>'
        else:
            return ""

    # displays a bullet if Czech texts are complete
    def has_language_cs(self):
        if (self.name_cs != "" and self.alias_cs != "" and self.description_cs != ""):
            return '<span style="font-size: 16pt;">&bull;</span>'
        else:
            return ""

    has_language_en.short_description = 'EN'
    has_language_de.short_description = 'DE'
    has_language_cs.short_description = 'CZ'
    has_language_en.allow_tags = True
    has_language_de.allow_tags = True
    has_language_cs.allow_tags = True


# ------------------------------------------------------------------------------
# HerbPicture model - images assigned to certain herb
#

# full path to /media/herbres
def picture_get_upload_path(instance, name):
    return instance._uploadname


class HerbPicture(models.Model):

    PICTURE_NAME_LENGTH = 16

    # picture widths for various devices
    PICTURE_WIDTHS = (120, 480, 768, 1080)

    _id             = models.AutoField(primary_key=True)
    author_id       = models.ForeignKey('herbapp.Author', default=1, verbose_name=_('Author'))
    herb_id         = models.ForeignKey('herbapp.Herb', verbose_name=_('Herb'))
    name            = models.CharField(default='', max_length=16, unique=True, editable=False, verbose_name=_('Filename'))
    picture         = models.ImageField(upload_to=picture_get_upload_path)
    timestamp       = models.DateTimeField(default=datetime.now, editable=False)

    class Meta:
        verbose_name = _('Herb picture')
        verbose_name_plural = _('Herb pictures')

    def __unicode__(self):
        return "%s" % self.name

    # return link to picture file with specific size
    def url(self, width = 0):
        src = self.picture.url
        if width > 0:
            src = "%s-%d%s" % (src[:-4], width, src[-4:])
        else:
            src = "%s%s" % (src[:-4], src[-4:])
        return src.replace(settings.MEDIA_ROOT + '/', '')
        
    # picture thumbnail for admin
    def thumbnail(self):
        src = settings.MEDIA_URL + self.url(120)
        return u'<a href="%s%s"><img style="max-width: 120px; max-height: 120px; " src="%s" /></a>' \
            % (settings.MEDIA_URL, self.url(), src )

    thumbnail.short_description = _('Thumbnail')
    thumbnail.allow_tags = True


    def save(self):

        if not self._id and not self.picture:
            return
        
        # generate a unique name (random string) for newly added picture
        if self.name == '':
            self.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(self.PICTURE_NAME_LENGTH))

        filepath, filename = os.path.split(self.picture.url)
        basename, ext = os.path.splitext(filename)
        ext = ext.lower()
        self._uploadname = os.path.join(settings.MEDIA_ROOT, 'herbres', "%s%s" % (self.name, ext))
        filepath, filename = os.path.split(self._uploadname)
        
        try:
            os.remove(self._uploadname)
        except:
            pass
        
        super(HerbPicture, self).save()

        exif = {}
        im = Image.open(self.picture.url)

        # rotate img as said by the EXIF orientation info
        exif_raw = None
        if ext.lower() == ".jpg":
            exif_raw = im._getexif()
        if exif_raw:
            for tag, value in exif_raw.items():
                decoded = PIL.ExifTags.TAGS.get(tag, tag)
                exif[decoded] = value

        if 'Orientation' in exif.keys():
            orientation = exif['Orientation']
            if orientation == 1:
                # Nothing
                mirror = im
            elif orientation == 2:
                # Vertical Mirror
                mirror = im.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                # Rotation 180°
                mirror = im.transpose(Image.ROTATE_180)
            elif orientation == 4:
                # Horizontal Mirror
                mirror = im.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                # Horizontal Mirror + Rotation 270°
                mirror = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
            elif orientation == 6:
                # Rotation 270°
                mirror = im.transpose(Image.ROTATE_270)
            elif orientation == 7:
                # Vertical Mirror + Rotation 270°
                mirror = im.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
            elif orientation == 8:
                # Rotation 90°
                mirror = im.transpose(Image.ROTATE_90)
        else:
            # No EXIF information, the user has to do it
            mirror = im

        ratio = mirror.size[1] / (float)(mirror.size[0])

        for width in self.PICTURE_WIDTHS:
            thumb = mirror.copy()
            size = (width, int(width * ratio))
            self.width, self.height = size
            filename = '%s/%s-%d%s' % (filepath, self.name, width, ext)

            thumb = thumb.resize(size, Image.ANTIALIAS)
            sharpener = ImageEnhance.Sharpness(thumb)
            thumb = sharpener.enhance(1.4)

            if ext == '.jpg':
                thumb.save(filename, "JPEG", quality = 90)
            else:
                thumb.save(filename)
                
        os.rename(filename, self._uploadname)


# ------------------------------------------------------------------------------
# HerbUsage model - forms of herb usage to cure various diseases
#

USAGE_CHOICES = (
    (0, ''),
    (1, _('tea')),
    (2, _('inhalation')),
    (3, _('gargle')),
    (4, _('bath')),
    (5, _('ointment')),
    (6, _('honey')),
    (7, _('poultice')),
    (8, _('oil')),
    (9, _('powder')),
    (10, _('syrup')),
    (11, _('liquere')),
    (12, _('juice')),
    (13, _('tincture')),
    (14, _('jam')),
    (15, _('chewing')),
)

class HerbUsage(models.Model):

    _id             = models.AutoField(primary_key=True)
    herb_id         = models.ForeignKey('herbapp.Herb', verbose_name=_('Herb'))
    disease_id      = models.ForeignKey('herbapp.Disease', verbose_name=_('Disease'))
    usage           = models.IntegerField(choices = USAGE_CHOICES, default=0, verbose_name=_('Usage'))
    timestamp       = models.DateTimeField(default=datetime.now, editable=False) # last change
    note_en         = models.CharField(max_length=200, blank=True, verbose_name=_('Note (EN)'))
    note_de         = models.CharField(max_length=200, blank=True, verbose_name=_('Note (DE)'))
    note_cs         = models.CharField(max_length=200, blank=True, verbose_name=_('Note (CS)'))
    note            = Translate

    class Meta:
        verbose_name = _('Herb usage')
        verbose_name_plural = _('Herb usages')

    def __unicode__(self):
        return "%s" % (self.disease_id.name)


# ------------------------------------------------------------------------------
# HerbPick model - what herb parts to collect and when
#

PART_CHOICES = (
    (0, ''),
    (1, _('root')),
    (2, _('bark')),
    (3, _('flower')),
    (4, _('leaf')),
    (5, _('needle')),
    (6, _('herb')),
    (7, _('fruit')),
    (8, _('resin')),
)

class HerbPick(models.Model):

    _id             = models.AutoField(primary_key=True)
    herb_id         = models.ForeignKey('herbapp.Herb', verbose_name=_('Herb'))
    herb_part       = models.IntegerField(choices = PART_CHOICES, default=0, verbose_name=_('Part'))
    month_from      = models.IntegerField(choices = MONTH_CHOICES, default=0, verbose_name=_('Pick from'))
    month_to        = models.IntegerField(choices = MONTH_CHOICES, default=0, verbose_name=_('Pick to'))
    timestamp       = models.DateTimeField(default=datetime.now, editable=False) # last change
    note_en         = models.CharField(max_length=200, blank=True, verbose_name=_('Note (EN)'))
    note_de         = models.CharField(max_length=200, blank=True, verbose_name=_('Note (DE)'))
    note_cs         = models.CharField(max_length=200, blank=True, verbose_name=_('Note (CS)'))
    note            = Translate

    class Meta:
        verbose_name = _('Herb pick')
        verbose_name_plural = _('Herb picks')

    def __unicode__(self):
        return "%s" % (self.get_herb_part_display())




from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete, post_delete
from django.dispatch import receiver
from _datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField, get_thumbnail


class OfficeRegion(models.Model):
    office_city = models.CharField(verbose_name='Оффис', max_length=255)

    class Meta:
        verbose_name = 'Оффисы'
        verbose_name_plural = 'Оффисы'

    def __str__(self):
        return "{}".format(self.office_city)


class Present(models.Model):
    present_name = models.CharField(verbose_name='Белектин аталышы', max_length=255)
    present_info = models.CharField(verbose_name='Белектин баяндамсы', max_length=255)
    present_date = models.DateTimeField(verbose_name='Берилген куну', auto_now_add=True)
    present_to = models.ForeignKey('CustomUser', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='gifts')

    def __str__(self):
        return "{}".format(self.present_name)


class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'


class CustomUser(AbstractUser):
    username_validator = MyValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    address = models.CharField(max_length=100, null=True,
                               blank=True)
    check_number = models.CharField(max_length=30, null=True,
                                    blank=True)
    check_image = models.ImageField(upload_to='images/', default='images/def.png',
                                    verbose_name='Сүрөт', null=True,
                                    blank=True)
    passport_number = models.CharField(max_length=20, null=True,
                                       blank=True)
    office_location = models.ForeignKey(OfficeRegion, related_name='offices',
                                        on_delete=models.SET_NULL, null=True,
                                        blank=True)
    by_whom = models.ForeignKey('self', related_name='users_by',
                                on_delete=models.SET_NULL, null=True,
                                blank=True)
    phone_number = models.CharField(max_length=60, null=True,
                                    blank=True)
    registration_date = models.DateTimeField(verbose_name='Дата регистрации', default=datetime.now)
    level = models.PositiveIntegerField(default=1)
    followers = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def clean_image(self):
        image_field = self.cleaned_data.get('image')
        if image_field:
            try:
                image_file = BytesIO(image_field.file.read())
                image = Image.open(image_file)
                image.thumbnail((300, 300), Image.ANTIALIAS)
                image_file = BytesIO()
                image.save(image_file, 'JPG', 'JPEG')
                image_field.file = image_file
                image_field.image = image

                return image_field
            except IOError:
                logger.exception("Error during resize image")


# Здесь реализовано Уровни паутины
# Если зарегистрироваться под кем-то то у него повысится фолловер +1
# После 3-х фолловеров будет 2-й уровен и больше не зафолловится

@receiver(pre_save, sender=CustomUser)
def followers_check(sender, instance, **kwargs):
    if instance.by_whom is None:
        pass
    elif instance.status is True:
        koe = CustomUser.objects.get(username=instance.by_whom)
        try:
            if koe.followers < 3:
                test = CustomUser.objects.filter(username=instance.by_whom).update(followers=koe.followers + 1)
        except:
            raise ValidationError('Followers error')
        try:
            if koe.followers == 2:
                test1 = CustomUser.objects.filter(username=instance.by_whom).update(level=koe.level + 1)
        except:
            raise ValidationError('Level error')

        if koe.by_whom is None:
            pass
        else:
            qwe = CustomUser.objects.get(username=koe.by_whom)
            sos = CustomUser.objects.filter(by_whom=CustomUser.objects.get(username=qwe.username))
            try:
                cnt = 0
                for x in sos:
                    if x.level == 2:
                        cnt += 1
                if cnt == 3:
                    test2 = CustomUser.objects.filter(username=qwe).update(level=3)
            except:
                raise ValidationError('Next level error')


@receiver(post_delete, sender=CustomUser)
def delete_check(sender, instance, **kwargs):
    if instance.by_whom is None:
        pass
    else:
        koe = CustomUser.objects.get(username=instance.by_whom)
        try:
            if koe.followers < 3:
                test = CustomUser.objects.filter(username=instance.by_whom).update(followers=koe.followers - 1)
        except:
            raise ValidationError('Followers error')
        try:
            if koe.followers == 3:
                test1 = CustomUser.objects.filter(username=instance.by_whom).update(level=koe.level - 1)
                test2 = CustomUser.objects.filter(username=instance.by_whom).update(followers=koe.followers - 1)
                if koe.by_whom is None:
                    pass
                else:
                    qwe = CustomUser.objects.get(username=koe.by_whom)
                    sos = CustomUser.objects.filter(by_whom=CustomUser.objects.get(username=qwe.username))
                    test2 = CustomUser.objects.filter(username=qwe).update(level=2)
        except:
            raise ValidationError('Level error')

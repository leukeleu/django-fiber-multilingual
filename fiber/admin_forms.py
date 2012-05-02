from django import forms
from django.utils.translation import ugettext_lazy as _

from mptt.forms import TreeNodeChoiceField

from multilingual.forms.forms import MultilingualModelForm

from app_settings import TEMPLATE_CHOICES, CONTENT_TEMPLATE_CHOICES
from models import Page, ContentItem
from utils.urls import is_quoted_url
from fiber.editor import get_editor_field_name


class ContentItemAdminForm(MultilingualModelForm):

    class Meta:
        model = ContentItem

        # Hack for multilingual: redefine fields here
        fields = ['name', get_editor_field_name('content_html'), 'template_name', 'protected', 'metadata']

    def __init__(self, *args, **kwargs):
        super(ContentItemAdminForm, self).__init__(*args, **kwargs)
        if len(CONTENT_TEMPLATE_CHOICES) > 0:
            self.fields['template_name'] = forms.ChoiceField(choices=CONTENT_TEMPLATE_CHOICES, required=False, label=_('Content template'))


class PageForm(MultilingualModelForm):

    parent = TreeNodeChoiceField(queryset=Page.tree.all(), level_indicator=3*unichr(160), empty_label='---------', required=False)
    redirect_page = TreeNodeChoiceField(label=_('Redirect page'), queryset=Page.objects.filter(redirect_page__isnull=True), level_indicator=3*unichr(160), empty_label='---------', required=False)

    class Meta:
        model = Page

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        if len(TEMPLATE_CHOICES) > 0:
            self.fields['template_name'] = forms.ChoiceField(choices=TEMPLATE_CHOICES, required=False, label=_('Template'))

    def clean_title(self):
        """
        Strips extra whitespace
        """
        return self.cleaned_data.get('title', '').strip()

    def clean_redirect_page(self):
        if self.cleaned_data['redirect_page']:
            try:
                if self.cleaned_data['url'] and is_quoted_url(self.cleaned_data['url']):
                    raise forms.ValidationError(_('A named url can\'t be combined with a redirect page'))
            except KeyError:
                pass
        return self.cleaned_data['redirect_page']

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from bakerydemo.breads.models import Country, BreadIngredient, BreadType
from bakerydemo.base.models import People, FooterText

from wagtail.core import hooks

# custom css to wagtailadmin
from django.templatetags.static import static
from django.utils.html import format_html

from wagtail.admin import widgets as wagtailadmin_widgets

from wagtail.admin.action_menu import ActionMenuItem



'''
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:

INSTALLED_APPS = (
   ...
   'wagtail.contrib.styleguide',
   ...
)

or see http://kave.github.io/general/2015/12/06/wagtail-streamfield-icons.html

This demo project includes the full font-awesome set via CDN in base.html, so the entire
font-awesome icon set is available to you. Options are at http://fontawesome.io/icons/.
'''


class BreadIngredientAdmin(ModelAdmin):
    # These stub classes allow us to put various models into the custom "Wagtail Bakery" menu item
    # rather than under the default Snippets section.
    model = BreadIngredient
    search_fields = ('name', )


class BreadTypeAdmin(ModelAdmin):
    model = BreadType
    search_fields = ('title', )


class BreadCountryAdmin(ModelAdmin):
    model = Country
    search_fields = ('title', )


class BreadModelAdminGroup(ModelAdminGroup):
    menu_label = 'Bread Categories'
    menu_icon = 'fa-suitcase'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (BreadIngredientAdmin, BreadTypeAdmin, BreadCountryAdmin)


class PeopleModelAdmin(ModelAdmin):
    model = People
    menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-users'  # change as required
    list_display = ('first_name', 'last_name', 'job_title', 'thumb_image')
    list_filter = ('job_title', )
    search_fields = ('first_name', 'last_name', 'job_title')


class FooterTextAdmin(ModelAdmin):
    model = FooterText
    search_fields = ('body',)


class BakeryModelAdminGroup(ModelAdminGroup):
    menu_label = 'Bakery Misc'
    menu_icon = 'fa-cutlery'  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (PeopleModelAdmin, FooterTextAdmin)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(BreadModelAdminGroup)
modeladmin_register(BakeryModelAdminGroup)


# customize admin panel (example only)
# it will hide leftbar items in admin panel
@hooks.register('construct_main_menu')
def hide_explorer_menu_item_from_username(request, menu_items):
  if request.user.username == 'user9':
    menu_items[:] = [item for item in menu_items if item.name != 'explorer']







"""Add custom .css hook to wagtail_admin"""
#from django.contrib.staticfiles.templatetags.staticfiles import static
#from django.utils.html import format_html

#from wagtail.core import hooks


# Register a custom css file for the wagtail admin.
@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/wagtail.css."""
    return format_html('<link rel="stylesheet" href="{}">', static("css/wagtail.css"))




@hooks.register('register_page_listing_more_buttons')
def page_listing_more_buttons(page, page_perms, is_parent=False):
    yield wagtailadmin_widgets.Button(
        'A dropdown button',
        '/goes/to/a/url/',
        priority=60
    )



@hooks.register('construct_page_action_menu')
def remove_unpublish_option(menu_items, request, context):
    menu_items[:] = [item for item in menu_items if item.name != 'action-unpublish']

@hooks.register('construct_page_action_menu')
def remove_submit_to_moderator_option(menu_items, request, context):
    menu_items[:] = [item for item in menu_items if item.name != 'action-submit']




class GuacamoleMenuItem(ActionMenuItem):
    label = "example link"

    def get_url(self, request, context):
        return "https://www.youtube.com/watch?v=dNJdJIwCF_Y"


@hooks.register('register_page_action_menu_item')
def register_guacamole_menu_item():
    return GuacamoleMenuItem(order=10)


'''
# add more welcome panel
from django.utils.safestring import mark_safe

#from wagtail.core import hooks

class WelcomePanel:
    order = 50

    def render(self):
        return mark_safe("""
        <section class="panel summary nice-padding">
          <h3>Just additional panel here.</h3>
        </section>
        """)

@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
  return panels.append( WelcomePanel() )
'''




from django.urls import reverse
from django.urls import reverse_lazy
#from wagtail.core import hooks
from wagtail.admin.menu import MenuItem

@hooks.register('register_admin_menu_item')
def register_user10_menu_item():
  return MenuItem('Go To Site', reverse_lazy('tagged_archive', kwargs={'page':'blog',}), classnames='icon icon-folder-inverse', order=10000)


#from django.urls import reverse
#from wagtail.core import hooks


'''
@hooks.register('register_account_menu_item')
def register_account_delete_account(request):
    return {
        'url': reverse('account_inactive'),
        'label': 'Delete account',
        'help_text': 'This permanently deletes your account.'
    }
'''


@hooks.register('filter_form_submissions_for_user')
def construct_forms_for_user(user, queryset):
    if not user.is_superuser:
        queryset = queryset.none()

    return queryset



class UserbarPuppyLinkItem:
    def render(self, request):
        return '<div class="wagtail-userbar__item " ><div class="wagtail-action wagtail-icon wagtail-icon-edit"><a href="https://drivedex.ru/" ' \
            + 'target="_parent" class="action icon icon-wagtail">GO HOME!</a></div></div>'

@hooks.register('construct_wagtail_userbar')
def add_puppy_link_item(request, items):
    return items.append(UserbarPuppyLinkItem())

'''
from wagtail.admin.userbar import AddPageItem, EditPageItem, ExplorePageItem

@hooks.register('construct_wagtail_userbar')
def delete_link_item(request, items):
        items[:] = [item for item in items if isinstance(item,EditPageItem)]
        for i in items:
            print('item', i.render(request))

'''




@hooks.register('register_page_listing_buttons')
def page_custom_listing_buttons(page, page_perms, is_parent=False):
    yield wagtailadmin_widgets.ButtonWithDropdownFromHook(
        'More Actions',
        hook_name='my_button_dropdown_hook',
        page=page,
        page_perms=page_perms,
        is_parent=is_parent,
        priority=50
    )

@hooks.register('my_button_dropdown_hook')
def page_custom_listing_more_buttons(page, page_perms, is_parent=False):
    if page_perms.can_move():
        yield wagtailadmin_widgets.Button('Move', reverse('wagtailadmin_pages:move', args=[page.id]), priority=10)
    if page_perms.can_delete():
        yield wagtailadmin_widgets.Button('Delete', reverse('wagtailadmin_pages:delete', args=[page.id]), priority=30)
    if page_perms.can_unpublish():
        yield wagtailadmin_widgets.Button('Unpublish', reverse('wagtailadmin_pages:unpublish', args=[page.id]), priority=40)


@hooks.register('construct_page_listing_buttons')
def delete_page_listing_button_items(buttons, page, page_perms, is_parent=False, context=None):
    #buttons[:] = [button for button in buttons if button != 'EDIT']
    buttons[:] = [button for button in buttons if button.label != 'Edit']
    #assert False
    for button in buttons:
        print(button.label)
    print(page.owner, 'pageeeeeeeeeeeeeeeeeeeeee')
    print(buttons)
@hooks.register('construct_page_listing_buttons')
def delete_page_listing_button_items(buttons, page, page_perms, is_parent=False, context=None):
        # buttons[:] = [button for button in buttons if button != 'EDIT']
        buttons[:] = [button for button in buttons if button.label != 'Редактировать']


@hooks.register('construct_page_listing_buttons')
def delete_page_listing_button_items(buttons, page, page_perms, is_parent=False, context=None):
    # buttons[:] = [button for button in buttons if button != 'EDIT']
    buttons[:] = [button for button in buttons if button.label != 'Смотреть на сайте']
@hooks.register('construct_page_listing_buttons')
def delete_page_listing_button_items(buttons, page, page_perms, is_parent=False, context=None):
    # buttons[:] = [button for button in buttons if button != 'EDIT']
    buttons[:] = [button for button in buttons if button.label != 'View live']



@hooks.register('construct_page_listing_buttons')
def delete_page_listing_button_items(buttons, page, page_perms, is_parent=False, context=None):
    # buttons[:] = [button for button in buttons if button != 'EDIT']
    buttons[:] = [button for button in buttons if button.label != 'View draft']
@hooks.register('construct_page_listing_buttons')
def delete_page_listing_button_items(buttons, page, page_perms, is_parent=False, context=None):
    # buttons[:] = [button for button in buttons if button != 'EDIT']
    buttons[:] = [button for button in buttons if button.label != 'Смотреть черновик']



@hooks.register('construct_page_listing_buttons')
def delete_page_listing_button_items(buttons, page, page_perms, is_parent=False, context=None):
    # buttons[:] = [button for button in buttons if button != 'EDIT']
    buttons[:] = [button for button in buttons if button.label != 'More']
@hooks.register('construct_page_listing_buttons')
def delete_page_listing_button_items(buttons, page, page_perms, is_parent=False, context=None):
    # buttons[:] = [button for button in buttons if button != 'EDIT']
    buttons[:] = [button for button in buttons if button.label != 'Больше']



@hooks.register('construct_page_listing_buttons')
def delete_page_listing_button_items(buttons, page, page_perms, is_parent=False, context=None):
    # buttons[:] = [button for button in buttons if button != 'EDIT']
    buttons[:] = [button for button in buttons if button.label != 'More Actions']
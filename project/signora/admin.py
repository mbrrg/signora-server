from django.contrib import admin
from signora.models import Device, Schedule, Content, Weekday
from django.conf import settings
from pusher import *

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1
    fields = [ 'valid_days', 'start', 'end', 'content' ]


def send_command(queryset, command):
    pusher = Pusher(app_id=settings.PUSHER_APP_ID, key=settings.PUSHER_APP_KEY, secret=settings.PUSHER_APP_SECRET)

    for device in queryset:
        channel = pusher["signora-{0}".format(device.identifier)]
        channel.trigger(command, dict())


def restart_device(modeladmin, request, queryset):
    send_command(queryset, "restart")
    restart_device.short_description = "Restart the selected devices"


def screen_off(modeladmin, request, queryset):
    send_command(queryset, "screenoff")
    screen_off.short_description = "Turn the screen off"


def screen_on(modeladmin, request, queryset):
    send_command(queryset, "screenon")
    screen_on.short_description = "Turn the screen on"

def reload_content(modeladmin, request, queryset):
    send_command(queryset, "reload")
    reload_content.short_description = "Reload content"

class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ['identifier', 'os', 'app_version', 'last_seen']
    fields = ['location', 'os', 'app_version']
    inlines = [ ScheduleInline ]
    list_display = [ 'ip_address', 'location', 'last_seen']
    actions = [restart_device, screen_on, screen_off, reload_content]

    def has_add_permission(self, request):
        return False


class ContentAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'static_url']

    def get_queryset(self, request):
        qs = super(ContentAdmin, self).get_queryset(request)
        return qs.filter(system_content=False)


admin.site.register(Device, DeviceAdmin)
admin.site.register(Content, ContentAdmin)

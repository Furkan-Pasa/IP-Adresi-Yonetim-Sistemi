from django.contrib import admin
from .models import Vlan, Device
from django import forms

# VLAN'ların Yönetim Paneli
class VlanAdmin(admin.ModelAdmin):
    list_display = ('vlan_name', 'vlan_value', 'start_ip_address', 'end_ip_address', 'netmask', 'description')
    search_fields = ('vlan_name', 'vlan_value', 'start_ip_address', 'end_ip_address', 'description')
    ordering = ('vlan_value',)
    list_per_page = 10


# Otomatik olarak ip adresini önermesi için kod
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'vlan' in self.initial:
            self.fields['ip_address'].widget = forms.Select(choices=self.get_available_ip_addresses(self.initial['vlan']))

    def get_available_ip_addresses(self, vlan_id):
        try:
            vlan = Vlan.objects.get(id=vlan_id)
            start_ip = vlan.start_ip_address
            end_ip = vlan.end_ip_address

            all_devices = Device.objects.filter(vlan=vlan)
            used_ips = set(device.ip_address for device in all_devices)

            all_ips = []
            start_int = self.ip_address_to_integer(start_ip)
            end_int = self.ip_address_to_integer(end_ip)

            for i in range(start_int, end_int + 1):
                ip = self.integer_to_ip_address(i)
                # Eğer düzenlenen kayıt ise kendi IP adresini değişime izin ver
                if ip not in used_ips or ip == self.instance.ip_address:  
                    all_ips.append((ip, ip))

            return all_ips

        except Vlan.DoesNotExist:
            pass
        return []


    def ip_address_to_integer(self, ip_address):
        parts = list(map(int, ip_address.split('.')))
        return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

    def integer_to_ip_address(self, integer):
        return '.'.join(str((integer >> i) & 255) for i in (24, 16, 8, 0))


# Cihazların Yönetim Paneli
class DeviceAdmin(admin.ModelAdmin):
    
    form = DeviceForm

    # Admin panelinde listelenecek alanların listesi:
    list_display = ('vlan', 'mac_address', 'ip_address', 'description', 'created_by', 'is_active')
    
    # Üst taraftaki arama çubuğunun hangi sütunlarda arama yapacağının listesi:
    search_fields = ('vlan', 'mac_address', 'ip_address', 'description', 'created_by')
    
    # Sağ taraftaki filtrede nelerin olacağının listesi:
    list_filter = ('vlan', 'created_by', 'is_active')

    # IP adresine göre küçükten büyüğe sıralama
    ordering = ('ip_address',)

    # Her sayfada 10 cihaz görüntüler
    list_per_page = 10

    # Yeni bir cihaz kaydedilirken, kaydeden kullanıcıyı belirler.
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    

# Admin panelinde görünecek modellerin listesi:
admin.site.register(Vlan, VlanAdmin)
admin.site.register(Device, DeviceAdmin)

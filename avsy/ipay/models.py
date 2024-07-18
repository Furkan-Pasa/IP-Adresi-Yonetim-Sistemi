from django.db import models
from django.contrib.auth.models import User

# VLAN listesi için tablo
class Vlan(models.Model):

    # VLAN ismi
    vlan_name = models.CharField(max_length=25, verbose_name="VLAN İsmi")
    # VLAN'ın sayısal değeri
    vlan_value = models.PositiveIntegerField(verbose_name="VLAN Numarası")

    # VLAN Başlangıç IP adresi
    start_ip_address = models.GenericIPAddressField(protocol='IPv4', verbose_name="Başlangıç IP Adresi")
    # VLAN Bitiş IP adresi
    end_ip_address = models.GenericIPAddressField(protocol='IPv4', verbose_name="Bitiş IP Adresi")
    # VLAN Netmask değeri
    netmask = models.GenericIPAddressField(protocol='IPv4', verbose_name="Netmask")

    # VLAN açıklaması
    description = models.TextField(max_length=150, verbose_name="Açıklama")

    def __str__(self):
        return self.vlan_name

    class Meta:
        verbose_name = "VLAN"
        verbose_name_plural = "VLAN'lar"



# Kayıt yapmış olan bir kullanıcı silindiğinde ne olacak?
def get_sentinel_user():
    # get_or_create deleted_user kullanıcısı varsa getir yoksa oluşturup getirir.
    return User.objects.get_or_create(username='deleted_user')[0]




# IP kaydı için kullanılacak tablo
class Device(models.Model):

    # ForeignKey -> ile her cihaz kaydının mutlaka bir vlana bağlanması gerekir.
    # on_delete=models.CASCADE -> eğer vlan silinirse o vlandaki tüm kayıtların da silinebilmesi için.
    vlan = models.ForeignKey(Vlan, on_delete=models.CASCADE, verbose_name="VLAN")

    # MAC adresleri 17 karakter olduğu için 17
    mac_address = models.CharField(max_length=17, unique=True, verbose_name="MAC Adresi")

    # Kaydedilecek cihaz için ayrılacak IP adresi
    ip_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True, unique=True, verbose_name="IP Adresi")

    # Kaydedilen cihaz için açıklama paragrafı
    description = models.TextField(max_length=150, verbose_name="Açıklama")

    # Cihaz kaydeden yetkilinin kullanıcı adı
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), blank=True, verbose_name="Kaydeden Kullanıcı")
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Kaydın aktiflik bilgisi
    is_active = models.BooleanField(default=True, verbose_name="Aktiflik Durumu")

    # Kaydın aktiflik bilgisi
    wireless = models.BooleanField(default=False, verbose_name="Kablosuz")

    def __str__(self):
        return f'{self.ip_address} - {self.mac_address}'

    class Meta:
        verbose_name = "Cihaz"
        verbose_name_plural = "KAYITLI CİHAZLAR"


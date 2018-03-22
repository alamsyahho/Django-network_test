from django import forms
import ipaddress

class NetworkTestForm(forms.Form):
    source = forms.CharField(max_length=20,help_text='Enter the source server IP address')
    destination = forms.CharField(max_length=20,help_text='Enter the destination server IP address')
    list= (
    ('tcp','TCP'),
    ('ntp','NTP'),
    ('dns','DNS'),
    )
    protocol = forms.ChoiceField(widget=forms.Select, choices=list, help_text='Choose protocol TCP or UDP')
    port = forms.IntegerField(min_value=1,max_value=65535,help_text='Enter destination port')

    def clean(self):
        cleaned_data = super(NetworkTestForm, self).clean()
        source = cleaned_data.get('source')
        destination = cleaned_data.get('destination')
        protocol = cleaned_data.get('protocol')

        for ip in source, destination:
            try:
                ipaddress.IPv4Address(ip)
            except:
                raise forms.ValidationError(ip + ' is not a valid ipv4 address')

        if not source and not destination and not port:
            raise forms.ValidationError('You have to write something!')

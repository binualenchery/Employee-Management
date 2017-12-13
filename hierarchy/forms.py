from django import forms

from .models import Designation
from django.db import connection

class SHierarchyForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Designation.objects.all())
   


class DesignationForm(forms.ModelForm):

    class Meta:
        model = Designation
        fields = ('name',)
        
class HierarchyForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Designation.objects.all())
    juniors = forms.ModelMultipleChoiceField(queryset=Designation.objects.all())

    def clean(self):
            cleaned_data = super().clean()
            name = cleaned_data.get('name')
            
            cursor = connection.cursor()
            cursor.execute("""SELECT id
            FROM hierarchy_designation
            WHERE name='%s' """ %name)
            
            data = cursor.fetchall()
            
            data = list(list(d) for d in data)
            name_id = data[0][0]
            
            dat = cleaned_data.get('juniors')
            juniors = list(dat.values_list(flat=True))

            if name_id and juniors:
                
                if name_id in juniors:
                    print('ccc')
                    raise forms.ValidationError(
                        "Cannot add %s as his own junior" % name
                        
                    )
                

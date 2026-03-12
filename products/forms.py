from django import forms
from .models import Medicine, ordereditems

class medicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'potency']

class orderedForm(forms.ModelForm):
    class Meta:
        model = ordereditems
        fields = ['order', 'customer','medicine', 'quantity']




git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ahm455/medical_store.git
git push -u origin main        
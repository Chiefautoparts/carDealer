from django import forms

class ContactForm(forms.Form):
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('sales', 'Sales - Vehicle Purchase'),
        ('service', 'Service & Maintenance'),
        ('financing', 'Financing & Loans'),
        ('trade_in', 'Trade-In Valuation'),
        ('parts', 'Parts & Accessories'),
    ]
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Full Name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(555) 123-4567'
        })
    )
    
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Please describe your inquiry or question...'
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Remove non-numeric characters for validation
        import re
        phone_digits = re.sub(r'\D', '', phone)
        if len(phone_digits) < 10:
            raise forms.ValidationError("Please enter a valid phone number with at least 10 digits.")
        return phone

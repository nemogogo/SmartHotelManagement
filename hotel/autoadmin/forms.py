from django.forms import ModelForm,fields
from django.utils.translation import ugettext as _
from django.forms import ValidationError
from hotel import models

from django import forms
from django.core.exceptions import ValidationError
def creat_model_form(request,model_admin):

    class Meta:
        model=model_admin.model
        fields="__all__"
    def default_clean(self):
        error_list = []
        self.ValidationError = ValidationError
        if not hasattr(model_admin, "is_add_form"):
            print("-------------------default_clean")
            for field in model_admin.readonly_fields:
                field_val = getattr(self.instance, field)
                field_from_page = self.cleaned_data.get(field)
                if field in model_admin.filter_horizontal:
                    field_val = getattr(self.instance, field).select_related()
                    # print(field_val)
                    field_val=str(field_val.order_by('id'))
                    field_from_page=str(field_from_page.order_by('id'))
                print( (field_val), field_from_page)
                if field_val!= field_from_page:
                    # error_list.append(ValidationError(
                    #     _("Field %(field)s is readonly,data should be %(val)s"),
                    #     code='invalid',
                    #     params={'field': field, 'val': field_val}
                    # ))
                    self.cleaned_data.get(field,field_val)
            if self.errors:
                for error, m in list(self.errors.items()):
                    if m.as_text() == '* This field is required.':
	                    self.errors.pop(error)
                
        response=model_admin.default_clean_form()
        if response:
            error_list.append(response)
        if error_list:
            raise ValidationError(error_list)
        
 
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
	        

            if not hasattr(model_admin, "is_add_form"):  # 代表这是添加form,不需要disabled
                if field_name in model_admin.readonly_fields:
                    field_obj.widget.attrs['disabled'] = 'disabled'
       
            if hasattr(model_admin,"clean_%s"%field_name):
                clean_func=getattr(model_admin,"clean_%s"%field_name)
                setattr(cls,"clean_%s"%field_name,clean_func)
	        
            field_obj.widget.attrs.update({'class': 'form-control'})
          
       
            
            if type(field_obj).__name__ in ['DateField','DateTimeField'] \
		            and not getattr(model_admin.model._meta.get_field(field_name),'auto_now_add',None) :
	            field_obj.widget.input_type='date'
		        
     
        return ModelForm.__new__(cls)

    _model_form_class=type("DynamicModelForm",(ModelForm,),{'Meta':Meta})

    setattr(_model_form_class, '__new__', __new__)
    setattr(_model_form_class, 'clean', default_clean)
   
  
    return _model_form_class


class UserCreationForm(ModelForm):
	
	
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
 
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model=models.UserProfile
        fields=['name','email','groups','role']
    def __new__(cls, *args, **kwargs):
	    for field_name, field_obj in cls.base_fields.items():
		    field_obj.widget.attrs.update({'class': 'form-control'})
	    return ModelForm.__new__(cls)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            from django.contrib.auth import models
            group = models.Group.objects.filter(name='staff')
            user.save()
            user.groups.add(*group)
        return user
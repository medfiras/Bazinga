from userena.forms import EditProfileForm
from userena import views as userena_views

class CustomEditProfileForm(userena_views.EditProfileForm):
	class Meta(EditProfileForm.Meta):
		exclude = EditProfileForm.Meta.exclude + ['privacy']
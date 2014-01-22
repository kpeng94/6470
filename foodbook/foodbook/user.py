from forms import ProfilePictureForm
from models import UserPicture
from django.core.files import File
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def upload_picture(request):
	if request.method == 'POST':
		form = ProfilePictureForm(request.POST, request.FILES)
		if form.is_valid():
			url = save_picture(request, request.FILES['image'])

def save_picture(request, image):
	pic = UserPicture.objects.filter(user_id=request.user)
	new_url = os.path.join(BASE_DIR, 'static/img/user/' + str(request.user.id))
	with open(new_url, 'wb') as destination:
		for chunk in image.chunks():
			destination.write(chunk)
	if not pic:
		new_pic = UserPicture(user_id=request.user, pic_link='/static/img/user/' + str(request.user.id))
		new_pic.save()
	else:
		pic[0].pic_link = '/static/img/user/' + str(request.user.id)
		pic[0].save()
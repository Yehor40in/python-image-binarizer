from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.textinput import TextInput

from io import BytesIO
from PIL import Image as PImage

IMG_DIR = 'D:\\Pictures\\'

class PhotoApp(App):
	path_to_img = TextInput(text='path to image', size_hint=(0.5, 0.2))
	rot_slider = Slider(min=0, max=360, value=0, size_hint=(0.3, 0.2))
	bin_slider = Slider(min=0, max=255, size_hint=(0.3, 0.2))
	view_area = BoxLayout(orientation='vertical')
	img_box = BoxLayout()
	edited_img = None
	
	pil_img = None
	pixels = None
	tmp_pixels = None
	tmp_image = None

	count = 1

	def build(self):
		self.view_area.add_widget(self.path_to_img)
		self.view_area.add_widget(Button(text='load', on_press=self.load_img, size_hint=(0.3, 0.3)))
		
		self.bin_slider.bind(value=self.binarize)
		self.view_area.add_widget(self.bin_slider)
		
		self.rot_slider.bind(value=self.rotate)
		self.view_area.add_widget(self.rot_slider)
		
		self.view_area.add_widget(Button(text='save', on_press=self.save_img, size_hint=(0.3, 0.3)))
		self.view_area.add_widget(self.img_box)

		return self.view_area

	def load_img(self, e):
		self.count = 0
		
		path = self.path_to_img.text.strip('\n')
		img_to_edit = Image(source=f'{IMG_DIR}{path}', id="proc_img")

		self.pil_img = PImage.open(f'{IMG_DIR}{path}')
		self.pixels = self.pil_img.load()

		self.tmp_image = PImage.open(f'{IMG_DIR}{path}')
		self.tmp_pixels = self.tmp_image.load()

		self.img_box.add_widget(img_to_edit)

	def binarize(self, instance, value):

		for i in range(self.pil_img.size[0]):
			for j in range(self.pil_img.size[1]):
				r, g, b = self.tmp_pixels[i,j]

				avg = (r + g + b)/3
				if avg < value:
					self.pixels[i,j] = (0, 0, 0)
				else:
					self.pixels[i,j] = (255, 255, 255)

		data = BytesIO()
		self.pil_img.save(data, format='png')
		data.seek(0)

		self.img_box.clear_widgets()
		img = CoreImage(BytesIO(data.read()), ext='png')
		self.img_box.add_widget(Image(texture=img.texture))

	def rotate(self, instance, value):
		rotated = self.pil_img.rotate(value)
		data = BytesIO()
		rotated.save(data, format='png')
		data.seek(0)

		self.img_box.clear_widgets()
		img = CoreImage(BytesIO(data.read()), ext='png')
		self.edited_img = Image(texture=img.texture)
		self.img_box.add_widget(self.edited_img)

	def save_img(self, e):
		path = self.path_to_img.text.split(".")[0]
		self.edited_img.export_to_png(f'{IMG_DIR}{path}{self.count}.png')
		self.count += 1

if __name__ == '__main__':
	PhotoApp().run()
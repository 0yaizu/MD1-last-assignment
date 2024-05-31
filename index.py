import py5, json, os, datetime, random
from pathlib import Path

frame_rate = 60

processing = {}
popup= []
display = ''
todo_list_path = ''

setting_json_data = {
	"todo_data": "",
	"frame_rate": frame_rate
}

current_dir = os.path.dirname(os.path.abspath(__file__))
print('Current Directory: ' + current_dir)

def first_setup():
	global display, frame_rate, processing, popup, todo_list_path
	# load font
	notoSans = py5.create_font(current_dir + '/NotoSansJP-VariableFont_wght.ttf', 60)
	py5.text_font(notoSans)
	# setting.jsonが無かった場合、生成
	if not os.path.isfile(current_dir + '/setting.json'):
		with open(current_dir + '/setting.json', mode='w', encoding='utf-8') as f:
			json.dump(setting_json_data, f, indent = 2)
		print('setting.json generated.')
	# todo_dataに記述(ディレクトリ)がない場合、新たに生成する
	with open(current_dir + '/setting.json', mode='r', encoding='utf-8') as f:
		settings = json.load(f)
		if settings['todo_data'] == '':
			display = 'loading'
			processing = {'process': 'create_to_do_file', 'next_screen': 'todo', 'wait_time': random.randint(60, 120)}
			# todo_list.json作成
			with open(current_dir + '/todo_list.json', mode='w', encoding='utf-8') as f:
				json.dump({}, f, indent = 2)
			print('todo_list.json generated.')
			# setting.jsonの内容取得
			with open(current_dir + '/setting.json', mode='r', encoding='utf-8') as f:
				current_settings = json.load(f)
			todo_list_path = Path(current_dir + '/todo_list.json')
			# setting.jsonにtodo_list.jsonのパスを記述(保存)
			with open(current_dir + '/setting.json', mode='w', encoding='utf-8') as f:
				current_settings['todo_data'] = '/todo_list.json'
				json.dump(current_settings, f, indent = 2)
		else:
			# todo_list.jsonを読み込み
			display = 'loading'
			processing = {'process': 'read_to_do_file', 'next_screen': 'todo', 'wait_time': 100}
			todo_list_path = Path(current_dir + settings['todo_data'])
			# setting.jsonの内容取得
			with open(current_dir + '/setting.json', mode='r', encoding='utf-8') as f:
				current_settings = json.load(f)
			todo_list_path = Path(current_dir + '/todo_list.json')
		# frame rate設定
		frame_rate = settings['frame_rate']
		if frame_rate == '' or not isinstance(frame_rate, int) or frame_rate == 0:
			frame_rate == 60
			print('[Warning] An incorrect value was entered for frame_rate.Please enter a valid value.')
		print(current_settings)

def setup():
	py5.size(800, 800, py5.P2D)
	py5.frame_rate(frame_rate)
	first_setup()
	py5.text('Now Loading...', py5.width / 2, py5.height / 2)		

def draw():
	global display, processing
	# reset
	py5.background(255)
	py5.text_align(py5.CENTER, py5.CENTER)
	py5.text_size(20)
	py5.stroke(0, 0, 0)
	py5.fill(0, 0, 0)
	# 表示部分
	# loading
	if display == 'loading':
		for i in range(5):
			w = 30 * py5.cos(py5.radians(4 * (py5.frame_count + i * 10)))
			h = 30 * py5.sin(py5.radians(4 * (py5.frame_count + i * 10)))
			py5.fill(0, 0, 0)
			py5.ellipse(py5.width / 2 + w, py5.height / 2 + h + 75, 10, 10)
			py5.fill(255, 255, 255, 70)
			py5.no_stroke()
			py5.rect(0, 0, py5.width, py5.height)
			py5.text_size(50)
			py5.fill(0, 0, 0)
			py5.text_align(py5.CENTER)
			py5.text('Now Loading...', py5.width / 2, py5.height / 2)
		if processing['wait_time'] > 0:
			processing['wait_time'] -= 1
		if processing['wait_time'] == 0:
			display = processing['next_screen']
			processing = {}
		return
	# todo
	if display == 'todo':
		py5.text_size(25)
		py5.fill(0, 0, 0)
		py5.text_align(py5.LEFT, py5.TOP)
		py5.text('todo List', 10, 10)
		py5.line(0, 40, py5.width, 40)
		return
	# error画面
	py5.text_size(50)
	py5.fill(0, 0, 0)
	py5.text_align(py5.CENTER)
	py5.text('an error occured.', py5.width / 2, py5.height / 2)

py5.run_sketch()
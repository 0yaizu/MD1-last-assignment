import py5, json, os, random, copy, math
from pathlib import Path

frame_rate = 60

mouse_info = {
	'x': 0,
	'y': 0,
	'button_pressed': False,
	'button_released': False
}

processing = {}
popup= []
display = ''
sub_display = ''
todo_list_path = ''
update_todo = {}
input_text = ''
cool_time = 0
add_todo_data = {
	"todo_name": "",
	"note": "",
	"date": ""
}

display_time = 0
current_settings = {}
setting_json_data = {
	"todo_data": "",
	"frame_rate": frame_rate
}

current_dir = os.path.dirname(os.path.abspath(__file__))
print('Current Directory: ' + current_dir)

def mouse_pressed():
	mouse_info['button_pressed'] = True

def mouse_released():
	mouse_info['button_released'] = True

def first_setup():
	global display, frame_rate, processing, popup, todo_list_path, current_settings
	# load font
	notoSans = py5.create_font(current_dir + '/NotoSansJP-VariableFont_wght.ttf', 60)
	py5.text_font(notoSans)
	# setting.jsonが無かった場合、生成
	if not os.path.isfile(current_dir + '/setting.json'):
		with open(current_dir + '/setting.json', mode='w', encoding='utf-8') as f:
			json.dump(setting_json_data, f, indent = 2)
			f.close()
		print('setting.json generated.')
	# todo_dataに記述(ディレクトリ)がない場合、新たに生成する
	with open(current_dir + '/setting.json', mode='r', encoding='utf-8') as f:
		settings = json.load(f)
		if settings['todo_data'] == '':
			display = 'loading'
			processing = {'process': 'create_to_do_file', 'next_screen': 'todo', 'wait_time': random.randint(15, 60)}
			# todo_list.json作成
			with open(current_dir + '/todo_list.json', mode='w', encoding='utf-8') as f:
				json.dump({
					"todo_name": "My ToDo",
					"todo_description": "This is a description of my ToDo item",
					"todo_list": []
				}, f, indent = 2)
				f.close()
			print('todo_list.json generated.')
			# setting.jsonの内容取得
			with open(current_dir + '/setting.json', mode='r', encoding='utf-8') as f:
				current_settings = json.load(f)
				f.close()
			todo_list_path = Path(current_dir + '/todo_list.json')
			# setting.jsonにtodo_list.jsonのパスを記述(保存)
			with open(current_dir + '/setting.json', mode='w', encoding='utf-8') as f:
				current_settings['todo_data'] = '/todo_list.json'
				json.dump(current_settings, f, indent = 2)
				f.close()
		else:
			# todo_list.jsonを読み込み
			display = 'loading'
			processing = {'process': 'read_to_do_file', 'next_screen': 'todo', 'wait_time': random.randint(20, 60)}
			todo_list_path = Path(current_dir + settings['todo_data'])
			# setting.jsonの内容取得
			with open(current_dir + '/setting.json', mode='r', encoding='utf-8') as f:
				current_settings = json.load(f)
				f.close()
			todo_list_path = Path(current_dir + '/todo_list.json')
		# frame rate設定
		frame_rate = settings['frame_rate']
		if frame_rate == '' or not isinstance(frame_rate, int) or frame_rate == 0:
			frame_rate == 60
			print('[Warning] An incorrect value was entered for frame_rate.Please enter a valid value.')
		print(current_settings)
		f.close()

def end_process():
	global mouse_info, cool_time
	# mouse info reset
	mouse_info['button_pressed'] = False
	mouse_info['button_released'] = False
	if cool_time > 0:
		cool_time -= 1

def setup():
	py5.size(800, 800, py5.P2D)
	py5.frame_rate(frame_rate)
	first_setup()
	py5.text('Now Loading...', py5.width / 2, py5.height / 2)		

def draw():
	global display, processing, current_settings, display_time, sub_display, input_text, add_todo_data, update_todo, mouse_info, cool_time
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
			display_time = 0
			processing = {}
		return
	# todo
	if display == 'todo':
		# header表示
		py5.text_size(25)
		py5.fill(0, 0, 0)
		py5.text_align(py5.LEFT, py5.TOP)
		py5.text('todo List', 10, 10)
		py5.line(0, 40, py5.width, 40)
		# todo add button
		py5.fill(255, 255, 255)
		if py5.width - 50 < py5.mouse_x < py5.width - 20 and 5 < py5.mouse_y < 35 and processing == {}:
			py5.fill(255, 165, 0)
		py5.rect_mode(py5.CORNER)
		py5.rect(py5.width - 50, 5, 30, 30)
		py5.fill(0, 0, 0)
		py5.line(py5.width - 35, 9, py5.width - 35, 31)
		py5.line(py5.width - 46, 20, py5.width - 23, 20)
		with open(current_dir + current_settings["todo_data"], mode='r', encoding='utf-8') as f:
			todo = json.load(f)
			if display_time == 1:
				print(json.dumps(todo["todo_list"], indent = 2))
			# todo list 表示
			for i in range(len(todo["todo_list"])):
				list_y = 100 + i * 75
				py5.fill(255, 255, 255)
				if 10 < py5.mouse_x < 30 and list_y - 10 < py5.mouse_y < list_y + 10 and processing == {}:
					py5.fill(255, 165, 0)
				py5.ellipse(20, list_y, 10, 10)
				# todo name
				py5.text_size(20)
				py5.fill(0, 0, 0)
				py5.text_align(py5.LEFT, py5.CENTER)
				py5.text(todo["todo_list"][i]["todo_name"], 40, list_y)
				# todo note
				py5.text_size(15)
				py5.fill(0, 0, 0)
				py5.text_align(py5.LEFT, py5.CENTER)
				py5.text(todo["todo_list"][i]["note"], 40, list_y + 25)
				# todo date
				py5.text_size(13)
				py5.fill(0, 0, 0)
				py5.text_align(py5.LEFT, py5.CENTER)
				py5.text(todo["todo_list"][i]["date"], 40, list_y - 20)
				# todo delete button
				if mouse_info['button_released'] == True and py5.mouse_button == py5.LEFT and 10 < py5.mouse_x < 30 and list_y - 10 < py5.mouse_y < list_y + 10 and cool_time == 0:
					update_todo = copy.deepcopy(todo)
					update_todo["todo_list"].pop(i)
					print('update:', todo)
					display_time = 0
					cool_time = math.floor(current_settings['frame_rate'] / 10)
					
			f.close()
			# todo_list.json更新
			if update_todo != {}:
				with open(current_dir + current_settings["todo_data"], mode='w', encoding='utf-8') as f:
					json.dump(update_todo, f, indent = 2, ensure_ascii = False)
					update_todo = {}
					f.close()
		# todo追加ボタン(押したら)
		if py5.is_mouse_pressed and py5.mouse_button == py5.LEFT and py5.width - 50 < py5.mouse_x < py5.width - 20 and 5 < py5.mouse_y < 35 and sub_display == '':
			sub_display = 'add_todo'
			processing = {'process': 'set_title'}
			input_text = ''
		# todo追加画面表示
		if sub_display == 'add_todo':
			py5.fill(255, 255, 255, 100)
			py5.no_stroke()
			py5.rect_mode(py5.CORNERS)
			py5.rect(0, 0, py5.width, py5.height)
			py5.fill(255, 255, 255)
			py5.stroke(0, 0, 0)
			py5.rect_mode(py5.CORNERS)
			py5.rect(100, 200, py5.width - 100, py5.height - 200)
			py5.fill(0, 0, 0)
			py5.text_size(18)
			py5.text_align(py5.LEFT, py5.TOP)
			py5.text('add todo', 110, 210)
			# set title
			if processing['process'] == 'set_title':
				if (input_text.endswith('\n') or input_text.endswith('\r\n') or input_text.endswith('\r')):
					if len(input_text[0:-1]) >= 1:
						sub_display = 'add_todo'
						processing = {'process': 'set_note'}
						add_todo_data['todo_name'] = input_text[0:-1]
						input_text = ''
					else:
						input_text = ''
				# set title表示
				py5.text_size(20)
				py5.text_align(py5.CENTER, py5.CENTER)
				py5.text('ToDo名を入力してください', py5.width / 2, 250)
				py5.fill(0, 0, 0)
				py5.line(150, py5.height / 2, py5.width - 150, py5.height / 2)
				py5.fill(0, 0, 0)
				py5.text_size(25)
				py5.text_align(py5.CENTER, py5.BOTTOM)
				py5.text(input_text, py5.width / 2, py5.height / 2 - 5)
			# set note
			if processing['process'] == 'set_note':
				if (input_text.endswith('\n') or input_text.endswith('\r\n') or input_text.endswith('\r')):
					display = 'todo'
					sub_display = 'add_todo'
					processing = {'process': 'set_date'}
					add_todo_data['note'] = input_text[0:-1]
					input_text = ''
				# set note表示
				py5.text_size(20)
				py5.text_align(py5.CENTER, py5.CENTER)
				py5.text('備考を入力してください', py5.width / 2, 250)
				py5.fill(0, 0, 0)
				py5.line(150, py5.height / 2, py5.width - 150, py5.height / 2)
				py5.fill(0, 0, 0)
				py5.text_size(25)
				py5.text_align(py5.CENTER, py5.BOTTOM)
				py5.text(input_text, py5.width / 2, py5.height / 2 - 5)
			# set date
			if processing['process'] == 'set_date':
				if (input_text.endswith('\n') or input_text.endswith('\r\n') or input_text.endswith('\r')):
					if len(input_text[0:-1]) >= 1:
						sub_display = ''
						processing = {}
						add_todo_data['date'] = input_text[0:-1]
						input_text = ''
						# todo_list.jsonを読み込み
						with open(current_dir + current_settings["todo_data"], mode='r', encoding='utf-8') as f:
							todo = json.load(f)
							todo["todo_list"].append(add_todo_data)
							f.close()
						# todo_list.jsonに追加、保存
						with open(current_dir + current_settings["todo_data"], mode='w', encoding='utf-8') as f:
							json.dump(todo, f, indent = 2, ensure_ascii = False)
							f.close()
						add_todo_data = {
							"todo_name": "",
							"note": "",
							"date": ""
						}
					else:
						input_text = ''
				# set date表示
				py5.text_size(20)
				py5.text_align(py5.CENTER, py5.CENTER)
				py5.text('時刻を入力してください', py5.width / 2, 250)
				py5.fill(0, 0, 0)
				py5.line(150, py5.height / 2, py5.width - 150, py5.height / 2)
				py5.fill(0, 0, 0)
				py5.text_size(25)
				py5.text_align(py5.CENTER, py5.BOTTOM)
				py5.text(input_text, py5.width / 2, py5.height / 2 - 5)
		display_time += 1
		end_process()
		return
	# error画面
	py5.text_size(50)
	py5.fill(0, 0, 0)
	py5.text_align(py5.CENTER)
	py5.text('an error occured.', py5.width / 2, py5.height / 2)

def key_pressed(e):
	global input_text
	pressed_key = e.get_key()
	if pressed_key != py5.CODED:
		if pressed_key == py5.BACKSPACE:
			if len(input_text) > 0:
				input_text = input_text[0:-1]
		else:
			input_text += pressed_key

py5.run_sketch()
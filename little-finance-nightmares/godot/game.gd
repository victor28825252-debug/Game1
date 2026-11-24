extends Control

const CREAM := Color("fff3d8")
const GOLD := Color("ffd17a")
const MINT := Color("9ce7da")
const NAVY := Color("101d2d")
const MAX_SCORE := 100
const FONT := preload("res://assets/NotoSansTC.ttf")

var level := 1
var scores: Array[int] = [0, 0]
var mistakes := 0
var hint_used := false
var hints_total := 0
var quiz_step := 0
var solved := false
var key_taken := false
var mode := "intro"
var ui_font: FontVariation
var previous_scores: Array[int] = []
var key_frames: Array[Texture2D] = []
var key_animation_time := 0.0

var backdrop: TextureRect
var hud: ColorRect
var hud_title: Label
var hud_score: Label
var action_note: Label
var desk_button: Button
var key_button: Button
var door_button: Button
var overlay: ColorRect
var card: PanelContainer
var card_content: VBoxContainer
var hint_button: Button

func _ready() -> void:
	_load_previous_scores()
	for i in range(8):
		key_frames.append(load("res://assets/key_frames/key_%02d.png" % i))
	ui_font = FontVariation.new()
	ui_font.base_font = FONT
	ui_font.variation_opentype = {"wght": 600}
	_build_ui()
	get_viewport().size_changed.connect(_layout)
	_show_intro()

func _process(delta: float) -> void:
	if key_button != null and key_button.visible and not key_frames.is_empty():
		key_animation_time += delta
		key_button.icon = key_frames[int(key_animation_time * 7.0) % key_frames.size()]

func _style(bg: Color, border: Color, radius: int = 18) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = bg
	s.border_color = border
	s.set_border_width_all(2)
	s.set_corner_radius_all(radius)
	s.content_margin_left = 18
	s.content_margin_right = 18
	s.content_margin_top = 12
	s.content_margin_bottom = 12
	return s

func _button(title: String, color: Color = Color("f6d188")) -> Button:
	var b := Button.new()
	b.text = title
	b.add_theme_font_size_override("font_size", 22)
	b.add_theme_font_override("font", ui_font)
	b.add_theme_color_override("font_color", NAVY)
	b.add_theme_color_override("font_hover_color", NAVY)
	b.add_theme_color_override("font_focus_color", NAVY)
	b.add_theme_color_override("font_hover_pressed_color", NAVY)
	b.add_theme_stylebox_override("normal", _style(color, Color("ffe7aa"), 14))
	b.add_theme_stylebox_override("hover", _style(color.lightened(.15), Color.WHITE, 14))
	b.add_theme_stylebox_override("pressed", _style(color.darkened(.12), GOLD, 14))
	b.add_theme_stylebox_override("focus", _style(Color.TRANSPARENT, Color.WHITE, 14))
	b.custom_minimum_size.y = 58
	b.focus_mode = Control.FOCUS_ALL
	return b

func _label(value: String, size: int, color: Color = CREAM) -> Label:
	var l := Label.new()
	l.text = value
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_font_override("font", ui_font)
	l.add_theme_color_override("font_color", color)
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return l

func _build_ui() -> void:
	backdrop = TextureRect.new()
	backdrop.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	backdrop.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	backdrop.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	add_child(backdrop)

	var shade := ColorRect.new()
	shade.color = Color(0, 0, 0, .13)
	shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(shade)

	hud = ColorRect.new()
	hud.color = Color("112337e8")
	add_child(hud)
	hud_title = _label("", 23, GOLD)
	hud.add_child(hud_title)
	hud_score = _label("", 21, MINT)
	hud_score.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	hud.add_child(hud_score)

	action_note = _label("", 22)
	action_note.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	action_note.add_theme_stylebox_override("normal", _style(Color("102237dc"), Color("4d898e"), 12))
	add_child(action_note)

	desk_button = _button("探索理財台", MINT)
	add_child(desk_button)
	desk_button.pressed.connect(_open_quiz)
	key_button = _button("取得金色鑰匙", GOLD)
	key_button.icon = key_frames[0]
	key_button.expand_icon = true
	key_button.icon_alignment = HORIZONTAL_ALIGNMENT_LEFT
	add_child(key_button)
	key_button.pressed.connect(_take_key)
	door_button = _button("前往下一間", GOLD)
	add_child(door_button)
	door_button.pressed.connect(_try_door)

	overlay = ColorRect.new()
	overlay.color = Color("071220dd")
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)
	card = PanelContainer.new()
	card.add_theme_stylebox_override("panel", _style(Color("142a3c"), GOLD, 24))
	overlay.add_child(card)
	card_content = VBoxContainer.new()
	card_content.add_theme_constant_override("separation", 15)
	card.add_child(card_content)
	_layout()

func _layout() -> void:
	var w := size.x
	var h := size.y
	hud.position = Vector2(24, 20)
	hud.size = Vector2(w - 48, 78)
	hud_title.position = Vector2(22, 18)
	hud_title.size = Vector2(maxf(100, w - 380), 42)
	hud_score.position = Vector2(maxf(100, w - 350), 18)
	hud_score.size = Vector2(300, 42)
	action_note.position = Vector2(w * .18, h - 98)
	action_note.size = Vector2(w * .64, 62)
	desk_button.position = Vector2(w * .19, h * .49)
	desk_button.size = Vector2(minf(240, w * .3), 65)
	key_button.position = Vector2(w * .47, h * .55)
	key_button.size = Vector2(minf(240, w * .3), 65)
	door_button.position = Vector2(w * .69, h * .43)
	door_button.size = Vector2(minf(240, w * .28), 65)
	card.size = Vector2(minf(w - 32, 740), minf(h - 35, 650))
	card.position = (Vector2(w, h) - card.size) / 2

func _clear_card() -> void:
	for c in card_content.get_children():
		card_content.remove_child(c)
		c.queue_free()

func _add_title(kicker: String, title: String, description: String) -> void:
	var k := _label(kicker, 18, MINT)
	k.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	card_content.add_child(k)
	var t := _label(title, 38, GOLD)
	t.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	card_content.add_child(t)
	var d := _label(description, 22)
	d.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	card_content.add_child(d)

func _show_intro() -> void:
	mode = "intro"
	overlay.visible = true
	desk_button.visible = false
	key_button.visible = false
	door_button.visible = false
	_clear_card()
	_add_title("兩間屋子・兩把鑰匙", "微光理財屋", "在溫柔的暗夜場景裡，解開生活理財謎題。每一關答對才能找到鑰匙，開門前進。")
	card_content.add_child(_label("第一關：零用錢與需要／想要\n第二關：儲蓄、投資與風險\n每關滿分 100 分；答錯可重試。", 21, MINT))
	var b := _button("開始探索")
	card_content.add_child(b)
	b.pressed.connect(_start)
	b.grab_focus()

func _start() -> void:
	level = 1
	scores = [0, 0]
	_begin_level()

func _begin_level() -> void:
	mode = "explore"
	mistakes = 0
	hint_used = false
	hints_total = 0
	quiz_step = 0
	solved = false
	key_taken = false
	backdrop.texture = load("res://assets/room_%d.png" % level)
	hud_title.text = "微光理財屋  /  第 %d 關：%s" % [level, "零用錢的房間" if level == 1 else "選擇的房間"]
	_update_score()
	action_note.text = "點選理財台，解開這一關的謎題。"
	overlay.visible = false
	desk_button.visible = true
	key_button.visible = false
	door_button.visible = true
	door_button.text = "開門前進" if level == 1 else "打開出口"
	desk_button.grab_focus()

func _update_score() -> void:
	var score := maxi(40, MAX_SCORE - mistakes * 20 - hints_total * 10)
	hud_score.text = "本關得分  %d / 100" % (scores[level - 1] if solved else score)

func _open_quiz() -> void:
	if solved:
		action_note.text = "謎題已解開。取得鑰匙，再前往門口。"
		return
	mode = "quiz"
	overlay.visible = true
	_show_quiz_step()

func _show_quiz_step() -> void:
	_clear_card()
	if level == 1:
		if quiz_step == 0:
			_add_title("第一關・生活預算  1 / 2", "零用錢怎麼安排？", "你有 100 元。午餐需要 45 元，還想至少存 30 元。哪個計畫可行？")
			_add_answer("午餐 45 元、玩具 60 元，之後再存錢", false)
			_add_answer("午餐 45 元、存 30 元、剩下 25 元自由安排", true)
			_add_answer("先買 80 元點心，再用剩下的錢吃午餐", false)
		else:
			_add_title("第一關・新的生活情境  2 / 2", "把方法用在新題目", "現在有 80 元。車費需 20 元、書本需 30 元，還想存 20 元。最多能花多少買想要的東西？")
			_add_answer("30 元，因為只要先付車費", false)
			_add_answer("50 元，因為書本下次再買", false)
			_add_answer("10 元，先留下車費、書本費和儲蓄", true)
	else:
		if quiz_step == 0:
			_add_title("第二關・儲蓄與風險  1 / 2", "哪個選擇比較穩當？", "你存了 200 元，下個月要繳 100 元材料費。現在有人邀你投資。你會怎麼做？")
			_add_answer("把 200 元全投入，因為對方說保證賺錢", false)
			_add_answer("借錢加碼，讓投資有機會更快變大", false)
			_add_answer("先留 100 元材料費；其餘先了解風險", true)
		else:
			_add_title("第二關・新的風險情境  2 / 2", "分散就一定安全嗎？", "兩個模擬投資都可能漲跌。把錢分到兩處後，下列哪句話比較正確？")
			_add_answer("分散可降低單一投資的影響，但仍可能虧損", true)
			_add_answer("只要分散，就能保證一定獲利", false)
			_add_answer("借更多錢分散，就完全沒有風險", false)
	hint_button = _button("我想看提示", Color("b7d5df"))
	card_content.add_child(hint_button)
	hint_button.pressed.connect(_show_hint)
	hint_button.disabled = hint_used
	if hint_used:
		card_content.add_child(_label("提示：" + _hint_text(), 19, MINT))
	var close := _button("先回房間", Color("c7d1d1"))
	card_content.add_child(close)
	close.pressed.connect(func(): overlay.visible = false; mode = "explore")

func _add_answer(value: String, correct: bool) -> void:
	var b := _button(value, Color("e3eff0"))
	b.add_theme_font_size_override("font_size", 19)
	card_content.add_child(b)
	b.pressed.connect(_answer.bind(correct))

func _show_hint() -> void:
	if hint_used:
		return
	hint_used = true
	hints_total += 1
	hint_button.disabled = true
	var l := _label("提示：" + _hint_text() + "（本關扣 10 分）", 19, MINT)
	card_content.add_child(l)
	_update_score()

func _hint_text() -> String:
	if level == 1:
		return "先扣必需費用與目標存款，再算剩餘。" if quiz_step == 0 else "80 − 20 − 30 − 20。"
	return "先留近期一定要用的錢。" if quiz_step == 0 else "分散不能消除所有風險。"

func _answer(correct: bool) -> void:
	if correct:
		if quiz_step == 0:
			quiz_step = 1
			hint_used = false
			_show_quiz_step()
			_update_score()
			return
		solved = true
		scores[level - 1] = maxi(40, MAX_SCORE - mistakes * 20 - hints_total * 10)
		_update_score()
		mode = "explore"
		overlay.visible = false
		desk_button.visible = false
		key_button.visible = true
		action_note.text = "答對了！金色鑰匙出現，請取得它。"
		key_button.grab_focus()
	else:
		mistakes += 1
		_update_score()
		var feedback := "先扣必需費用，再算可花與可存的餘額。" if level == 1 else "投資有風險；分散也不能保證獲利。"
		var l := _label("再想想：" + feedback + "（本關扣 20 分）", 19, Color("ffb9a1"))
		card_content.add_child(l)

func _take_key() -> void:
	if not solved:
		return
	key_taken = true
	key_button.visible = false
	action_note.text = "你取得鑰匙了！點選右側的門繼續。"
	door_button.grab_focus()

func _try_door() -> void:
	if not key_taken:
		action_note.text = "門還鎖著。先在理財台解題，並取得鑰匙。"
		return
	if level == 1:
		level = 2
		_begin_level()
	else:
		_show_results()

func _show_results() -> void:
	mode = "result"
	overlay.visible = true
	desk_button.visible = false
	key_button.visible = false
	door_button.visible = false
	_clear_card()
	var progress := "第一次完成：已建立練習基準。再玩一次可比較同一關表現。"
	if previous_scores.size() == 2:
		progress = "與上次同關相比：預算 %s；風險 %s。" % [_difference_text(scores[0] - previous_scores[0]), _difference_text(scores[1] - previous_scores[1])]
	_add_title("兩把鑰匙都取得了", "你的理財成長報告", "預算關：%d / 100     風險關：%d / 100\n%s" % [scores[0], scores[1], progress])
	card_content.add_child(_label("本次練習成果：\n• 先照顧需要，再安排想要與儲蓄。\n• 保留近期必需費用，了解投資風險。\n分數代表遊戲表現，不單獨證明學習成效。", 21, MINT))
	var total := _label("總分  %d / 200" % (scores[0] + scores[1]), 29, GOLD)
	total.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	card_content.add_child(total)
	var again := _button("再挑戰一次")
	card_content.add_child(again)
	again.pressed.connect(_start)
	again.grab_focus()
	_save_scores()

func _difference_text(delta: int) -> String:
	if delta > 0:
		return "進步 %d 分" % delta
	if delta < 0:
		return "少 %d 分" % -delta
	return "維持同分"

func _load_previous_scores() -> void:
	if not FileAccess.file_exists("user://finance_scores.json"):
		return
	var f := FileAccess.open("user://finance_scores.json", FileAccess.READ)
	if f == null:
		return
	var data = JSON.parse_string(f.get_as_text())
	if data is Dictionary and data.has("scores") and data["scores"] is Array and data["scores"].size() == 2:
		previous_scores = [int(data["scores"][0]), int(data["scores"][1])]

func _save_scores() -> void:
	var f := FileAccess.open("user://finance_scores.json", FileAccess.WRITE)
	if f != null:
		f.store_string(JSON.stringify({"scores": scores, "version": 2}))
		f.close()
	previous_scores = scores.duplicate()

func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE and mode == "quiz":
		overlay.visible = false
		mode = "explore"

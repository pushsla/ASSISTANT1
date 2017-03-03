#!/usr/bin/python3
import urwid, subprocess
def exit_on_q(key):
	if key in ('q', 'Q'):
		subprocess.terminate()
		raise urwid.ExitMainLoop()
def gui():
	req = u"Fluffy@Fluffy_Brick$ Привет. Я УПК(Умный Пушистый Кирпич). Беда в том, что я понимаю не любые формы запросов... \n Скажи 'Кирпич..!', и я начну тебя слушать. Если хочешь спросить о чём-то, скажи 'вопрос'. Можешь так же спросить меня: 'погода в городе москва', например. Еще я могу перевести фразу на английский или русский язык: 'переведи на английский',- например, - 'язык...'\n Чтобы закрыть меня, нажми 'Q'\n <аза-за-за-за. Ты только что попробовал нажать Q> }:) Ctrl+C рулит."
	palette = [
		('banner', '', '', '', '#fff', '#11b'),
		('streak', '', '', '', 'g50', '#11b'),
		('inside', '', '', '', 'g38', '#228'),
		('outside', '', '', '', 'g27', '#225'),
		('bg', '', '', '', 'g7', '#222'),]
	placeholder = urwid.SolidFill()
	loop = urwid.MainLoop(placeholder, palette, unhandled_input=exit_on_q)
	loop.screen.set_terminal_properties(colors=256)
	loop.widget = urwid.AttrMap(placeholder, 'bg')
	loop.widget.original_widget = urwid.Filler(urwid.Pile([]))

	div = urwid.Divider()
	outside = urwid.AttrMap(div, 'outside')
	inside = urwid.AttrMap(div, 'inside')
	txt = urwid.Text(('banner', req), align='center')
	streak = urwid.AttrMap(txt, 'streak')
	pile = loop.widget.base_widget # .base_widget skips the decorations
	for item in [outside, inside, streak, inside, outside]:
		pile.contents.append((item, pile.options()))
	loop.run()

#subprocess.Popen('./main.py')
gui()
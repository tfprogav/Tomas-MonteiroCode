from tkinter import *
from tkinter import ttk

import janela_avaliacao
import janela_performance


def show_gestao_utilizadores():
    clear_content_frame()
    label = Label(content_frame, text='Informações de Gestão de Utilizadores', font=('Arial', 14))
    label.pack(pady=20)

def show_gestao_alunos():
    clear_content_frame()
    label = Label(content_frame, text='Informações de Gestão de Alunos', font=('Arial', 14))
    label.pack(pady=20)

def show_gestao_aulas_horarios():
    clear_content_frame()
    label = Label(content_frame, text='Informações de Gestão de Aulas e Horários', font=('Arial', 14))
    label.pack(pady=20)

def show_gestao_pagamentos():
    clear_content_frame()
    label = Label(content_frame, text='Informações de Gestão de Pagamentos', font=('Arial', 14))
    label.pack(pady=20)

def show_avaliacao_alunos():
    clear_content_frame()
    label = Label(content_frame, text='Informações de Avaliação de Alunos', font=('Arial', 14))
    label.pack(pady=20)

def show_performance_alunos():
    clear_content_frame()
    label = Label(content_frame, text='Informações de Performance de Alunos', font=('Arial', 14))
    label.pack(pady=20)

def clear_content_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

root = Tk()
root.title('Centro de formação')
root.geometry('1280x640+280+150')
root.resizable(0, 0)

FONT = ('Arial', 12)

main_frame = Frame(root, width=1280, height=720, bg='#F5F5F5')
main_frame.pack(fill='both', expand=True)

menu_frame = Frame(main_frame, bg='#383838', width=200, height=720)
menu_frame.pack(side='left', fill='y')

content_frame = Frame(main_frame, bg='white', width=1080, height=720)
content_frame.pack(side='left', fill='both', expand=True)

button_styles = {
    'bg': '#008080',
    'fg': 'white',
    'activebackground': '#4C4C4C',
    'activeforeground': 'white',
    'font': FONT,
    'borderwidth': 0,
    'highlightthickness': 0,
    'relief': 'flat',
    'cursor': 'hand2',
}

button1 = Button(menu_frame, text='Gestão de Utilizadores', **button_styles, command=show_gestao_utilizadores)
button1.pack(pady=10, padx=20, fill='x')

button2 = Button(menu_frame, text='Gestão de Alunos', **button_styles, command=show_gestao_alunos)
button2.pack(pady=10, padx=20, fill='x')

button3 = Button(menu_frame, text='Gestão de Aulas e Horários', **button_styles, command=show_gestao_aulas_horarios)
button3.pack(pady=10, padx=20, fill='x')

button4 = Button(menu_frame, text='Gestão de Pagamentos', **button_styles, command=show_gestao_pagamentos)
button4.pack(pady=10, padx=20, fill='x')

button5 = Button(menu_frame, text='Gestão de Avaliações', **button_styles, command=lambda: janela_avaliacao.gestao_avaliacoes(content_frame))
button5.pack(pady=10, padx=20, fill='x')

button6 = Button(menu_frame, text='Performance de Alunos', **button_styles, command=lambda: janela_performance.gestao_performance(content_frame))
button6.pack(pady=10, padx=20, fill='x')

root.mainloop()
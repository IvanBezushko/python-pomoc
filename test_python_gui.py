#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program testowy Python - GUI z bazą pytań
"""

import json
import random
import datetime
from pathlib import Path
from tkinter import (
    Tk, ttk, Frame, Label, Button, Radiobutton, StringVar, 
    Text, Scrollbar, messagebox, font, Canvas
)

# Kolory
COLOR_CORRECT = "#2d5016"  # ciemnozielony
COLOR_INCORRECT = "#8b1a1a"  # ciemnoczerwony
COLOR_BG = "#ffffff"  # biały
COLOR_LIGHT = "#f5f5f5"
COLOR_DARK = "#333333"


class TestPythonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Python - Zaliczenie")
        self.root.geometry("1000x800")
        self.root.configure(bg=COLOR_BG)
        
        # Załaduj pytania
        self.questions = self.load_questions()
        
        # Historia testów
        self.history_file = Path(__file__).parent / "test_python_historia.json"
        self.history = self.load_history()
        
        # Stan testu
        self.current_test = None
        self.current_question_index = 0
        self.user_answers = []
        self.test_start_time = None
        
        # Załaduj teorię
        self.theory_content = self.load_theory()
        
        # Styl
        self.setup_styles()
        
        # GUI
        self.create_widgets()
        
    def setup_styles(self):
        """Konfiguracja stylów"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Białe tło dla zakładek
        style.configure('TNotebook', background=COLOR_BG, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10], background=COLOR_LIGHT)
        style.map('TNotebook.Tab', background=[('selected', COLOR_BG)])
        
    def load_questions(self):
        """Załaduj pytania z JSON"""
        json_file = Path(__file__).parent / "test_python_baza_pytan.json"
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Błąd", f"Nie znaleziono pliku: {json_file}")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Błąd", "Błąd odczytu pliku JSON")
            return []
    
    def load_history(self):
        """Załaduj historię testów"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def load_theory(self):
        """Załaduj teorię z pliku markdown"""
        theory_file = Path(__file__).parent / "SCIAGA_PYTHON.md"
        try:
            with open(theory_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Nie znaleziono pliku SCIAGA_PYTHON.md"
        except Exception as e:
            return f"Błąd odczytu pliku: {e}"
    
    def save_history(self):
        """Zapisz historię testów"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def create_widgets(self):
        """Utwórz główne widgety"""
        # Notebook (zakładki)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Zakładka 1: Test
        self.frame_test = Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(self.frame_test, text="📝 Test")
        self.create_test_tab()
        
        # Zakładka 2: Historia
        self.frame_history = Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(self.frame_history, text="📊 Historia")
        self.create_history_tab()
        
        # Zakładka 3: Teoria
        self.frame_theory = Frame(self.notebook, bg=COLOR_BG)
        self.notebook.add(self.frame_theory, text="📚 Teoria")
        self.create_theory_tab()
    
    def create_test_tab(self):
        """Utwórz zakładkę testu"""
        # Nagłówek
        header = Frame(self.frame_test, bg=COLOR_BG)
        header.pack(fill='x', pady=(10, 20))
        
        title = Label(
            header, 
            text="Test Python - 20 pytań",
            font=font.Font(size=20, weight='bold'),
            bg=COLOR_BG,
            fg=COLOR_DARK
        )
        title.pack()
        
        self.label_info = Label(
            header,
            text="Kliknij 'Rozpocznij test' aby rozpocząć",
            font=font.Font(size=11),
            bg=COLOR_BG,
            fg=COLOR_DARK
        )
        self.label_info.pack(pady=5)
        
        # Ramka z scrollowaniem dla treści
        canvas_frame = Frame(self.frame_test, bg=COLOR_BG)
        canvas_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Canvas z scrollbarem
        canvas = Canvas(canvas_frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=COLOR_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Funkcja do aktualizacji scrollowania
        def update_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Ustaw szerokość scrollable_frame na szerokość canvas
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        scrollable_frame.bind("<Configure>", update_scroll)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        
        # Scrollowanie kółkiem myszy
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Zapisz canvas dla późniejszego użycia
        self.test_canvas = canvas
        
        # Główna ramka z pytaniem - wewnątrz scrollowalnego obszaru
        self.frame_question = scrollable_frame
        
        # Pytanie - responsywne, dostosowuje się do zawartości
        self.text_question = Text(
            self.frame_question,
            wrap='word',
            font=font.Font(size=12),
            bg=COLOR_LIGHT,
            fg=COLOR_DARK,
            relief='flat',
            padx=15,
            pady=15,
            width=1,  # Minimalna szerokość, będzie się dostosowywać
            height=1  # Minimalna wysokość, będzie się dostosowywać
        )
        self.text_question.pack(fill='both', expand=True, pady=(0, 10))
        self.text_question.config(state='disabled')
        
        # Osobne pole dla kodu (monospace, jak w edytorze) - tworzymy ale ukryjemy domyślnie
        self.code_label = Label(
            self.frame_question,
            text="Kod:",
            font=font.Font(size=10, weight='bold'),
            bg=COLOR_BG,
            fg=COLOR_DARK,
            anchor='w'
        )
        # Nie packujemy jeszcze - będzie pokazane tylko gdy jest kod
        
        # Frame dla kodu z scrollbarem
        self.code_frame = Frame(self.frame_question, bg=COLOR_BG)
        # Nie packujemy jeszcze - będzie pokazane tylko gdy jest kod
        
        self.text_code = Text(
            self.code_frame,
            wrap='none',  # Brak zawijania dla kodu
            font=font.Font(family='Consolas', size=10),
            bg="#2B2B2B",  # Ciemne tło jak w edytorze
            fg="#A9B7C6",  # Jasny tekst
            height=8,
            relief='flat',
            padx=15,
            pady=15,
            insertbackground="#FFFFFF"  # Kolor kursora
        )
        
        # Scrollbar dla pola kodu
        self.code_scrollbar = Scrollbar(
            self.code_frame,
            orient="vertical",
            command=self.text_code.yview,
            bg="#404040",
            troughcolor="#1E1E1E",
            activebackground="#606060",
            width=12
        )
        self.text_code.configure(yscrollcommand=self.code_scrollbar.set)
        self.text_code.config(state='disabled')
        
        # Pakowanie scrollbara i tekstu
        self.text_code.pack(side="left", fill="both", expand=True)
        self.code_scrollbar.pack(side="right", fill="y")
        # Nie packujemy code_frame jeszcze - będzie pokazane tylko gdy jest kod
        
        # Odpowiedzi (radio buttons)
        self.frame_answers = Frame(self.frame_question, bg=COLOR_BG)
        self.frame_answers.pack(fill='x', pady=(0, 15))
        
        self.answer_var = StringVar(value="")  # Odznaczone domyślnie
        self.radio_buttons = []
        
        # Wynik poprzedniego pytania
        self.frame_result = Frame(self.frame_question, bg=COLOR_BG)
        self.frame_result.pack(fill='x', pady=(0, 15))
        
        self.label_result = Label(
            self.frame_result,
            text="",
            font=font.Font(size=11, weight='bold'),
            bg=COLOR_BG,
            wraplength=800
        )
        self.label_result.pack()
        
        self.text_explanation = Text(
            self.frame_result,
            wrap='word',
            font=font.Font(size=10),
            bg=COLOR_LIGHT,
            height=3,
            relief='flat',
            padx=10,
            pady=10
        )
        self.text_explanation.pack(fill='x', pady=(5, 0))
        self.text_explanation.config(state='disabled')
        
        # Przyciski - POZA scrollowaniem, zawsze widoczne na dole
        self.frame_buttons = Frame(self.frame_test, bg=COLOR_BG)
        self.frame_buttons.pack(fill='x', padx=20, pady=(10, 15), side='bottom')
        
        self.btn_start = Button(
            self.frame_buttons,
            text="▶ Rozpocznij test",
            font=font.Font(size=12, weight='bold'),
            bg="#4CAF50",
            fg="white",
            relief='flat',
            padx=30,
            pady=10,
            command=self.start_test
        )
        self.btn_start.pack(side='left', padx=5)
        
        self.btn_submit = Button(
            self.frame_buttons,
            text="✓ Zatwierdź odpowiedź",
            font=font.Font(size=12, weight='bold'),
            bg="#2196F3",
            fg="white",
            relief='flat',
            padx=30,
            pady=10,
            command=self.submit_answer,
            state='disabled'
        )
        self.btn_submit.pack(side='left', padx=5)
        
        self.btn_next = Button(
            self.frame_buttons,
            text="⏭ Następne pytanie",
            font=font.Font(size=12, weight='bold'),
            bg="#FF9800",
            fg="white",
            relief='flat',
            padx=30,
            pady=10,
            command=self.next_question,
            state='disabled'
        )
        self.btn_next.pack(side='left', padx=5)
    
    def create_history_tab(self):
        """Utwórz zakładkę historii"""
        header = Label(
            self.frame_history,
            text="Historia testów",
            font=font.Font(size=18, weight='bold'),
            bg=COLOR_BG,
            fg=COLOR_DARK
        )
        header.pack(pady=20)
        
        # Ramka z listą
        frame_list = Frame(self.frame_history, bg=COLOR_BG)
        frame_list.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = Scrollbar(frame_list)
        scrollbar.pack(side='right', fill='y')
        
        # Lista testów
        self.text_history = Text(
            frame_list,
            wrap='word',
            font=font.Font(size=10),
            bg=COLOR_LIGHT,
            fg=COLOR_DARK,
            yscrollcommand=scrollbar.set,
            relief='flat',
            padx=15,
            pady=15
        )
        self.text_history.pack(fill='both', expand=True)
        self.text_history.config(state='disabled')
        scrollbar.config(command=self.text_history.yview)
        
        # Przycisk odśwież
        btn_refresh = Button(
            self.frame_history,
            text="🔄 Odśwież historię",
            font=font.Font(size=11),
            bg="#9E9E9E",
            fg="white",
            relief='flat',
            padx=20,
            pady=8,
            command=self.refresh_history
        )
        btn_refresh.pack(pady=10)
        
        self.refresh_history()
    
    def create_theory_tab(self):
        """Utwórz zakładkę teorii - wyświetl bezpośrednio zawartość"""
        header = Label(
            self.frame_theory,
            text="Teoria Python",
            font=font.Font(size=18, weight='bold'),
            bg=COLOR_BG,
            fg=COLOR_DARK
        )
        header.pack(pady=20)
        
        # Ramka z teorią
        frame_theory_container = Frame(self.frame_theory, bg=COLOR_BG)
        frame_theory_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = Scrollbar(frame_theory_container)
        scrollbar.pack(side='right', fill='y')
        
        # Tekst teorii
        self.text_theory = Text(
            frame_theory_container,
            wrap='word',
            font=font.Font(size=11),
            bg=COLOR_LIGHT,
            fg=COLOR_DARK,
            yscrollcommand=scrollbar.set,
            relief='flat',
            padx=15,
            pady=15
        )
        self.text_theory.pack(fill='both', expand=True)
        
        scrollbar.config(command=self.text_theory.yview)
        
        # Wstaw zawartość teorii
        self.text_theory.config(state='normal')
        self.text_theory.delete(1.0, 'end')
        self.text_theory.insert(1.0, self.theory_content)
        self.text_theory.config(state='disabled')
    
    def start_test(self):
        """Rozpocznij nowy test"""
        # Losuj 20 pytań
        selected = random.sample(self.questions, min(20, len(self.questions)))
        
        self.current_test = {
            'questions': selected,
            'answers': [],
            'correct': 0,
            'start_time': datetime.datetime.now().isoformat()
        }
        
        self.user_answers = []
        self.current_question_index = 0
        self.test_start_time = datetime.datetime.now()
        
        # Aktualizuj GUI
        self.label_info.config(text=f"Pytanie 1/20")
        self.btn_start.config(state='disabled')
        self.btn_submit.config(state='normal')
        self.btn_next.config(state='disabled')
        
        self.show_question(0)
    
    def show_question(self, index):
        """Wyświetl pytanie"""
        if index >= len(self.current_test['questions']):
            self.finish_test()
            return
        
        question = self.current_test['questions'][index]
        
        # Wyczyść poprzednie wyniki
        self.label_result.config(text="")
        self.text_explanation.config(state='normal')
        self.text_explanation.delete(1.0, 'end')
        self.text_explanation.config(state='disabled')
        
        # Ukryj pole kodu domyślnie
        self.code_frame.pack_forget()
        self.code_label.pack_forget()
        
        # Sprawdź czy jest kod w pytaniu
        pytanie_text = question['pytanie']
        code_snippet = None
        
        if '```python' in pytanie_text:
            # Wyodrębnij kod
            parts = pytanie_text.split('```python')
            pytanie_bez_kodu = parts[0].strip()
            
            if len(parts) > 1:
                code_part = parts[1].split('```')[0].strip()
                code_snippet = code_part
                
                # Wyświetl pytanie bez kodu
                typ_emoji = "💻" if question['typ'] == 'kod' else "📖"
                pytanie_display = f"{typ_emoji} {question['typ'].upper()}\n\n{pytanie_bez_kodu}"
                
                # Pokaż etykietę i pole kodu
                self.code_label.pack(fill='x', pady=(10, 5), before=self.frame_answers)
                
                # Wyświetl kod w osobnym polu - jak w edytorze
                self.text_code.config(state='normal')
                self.text_code.delete(1.0, 'end')
                self.text_code.insert(1.0, code_snippet)
                
                # Ustaw dynamiczną wysokość na podstawie liczby linii (min 10, max 35 linii)
                # Zwiększamy maksymalną wysokość, aby pokazać więcej kodu na raz
                num_lines = code_snippet.count('\n') + 1
                code_height = max(10, min(35, num_lines + 3))  # +3 dla marginesu, max 35 linii
                self.text_code.config(height=code_height)
                
                # Jeśli kod jest dłuższy niż maksymalna wysokość, scrollbar będzie widoczny
                # Przewiń na górę, aby pokazać początek kodu
                self.text_code.see("1.0")
                
                self.text_code.config(state='disabled')
                # Pakuj frame z kodem i scrollbarem
                self.code_frame.pack(fill='both', expand=True, pady=(0, 15), before=self.frame_answers)
        else:
            # Pytanie bez kodu
            typ_emoji = "💻" if question['typ'] == 'kod' else "📖"
            pytanie_display = f"{typ_emoji} {question['typ'].upper()}\n\n{pytanie_text}"
        
        # Wyświetl pytanie
        self.text_question.config(state='normal')
        self.text_question.delete(1.0, 'end')
        self.text_question.insert(1.0, pytanie_display)
        
        # Oblicz liczbę linii i dostosuj wysokość dynamicznie
        # Użyj update_idletasks aby zaktualizować rozmiar widgetu przed obliczeniem
        self.text_question.update_idletasks()
        num_lines = int(self.text_question.index('end-1c').split('.')[0])
        # Większy zakres - min 4 linie, max 30 linii aby pomieścić długie pytania
        question_height = max(4, min(30, num_lines + 2))
        self.text_question.config(height=question_height)
        
        self.text_question.config(state='disabled')
        
        # Usuń stare radio buttons
        for rb in self.radio_buttons:
            rb.destroy()
        self.radio_buttons = []
        
        # Utwórz nowe radio buttons - upewnij się, że są odznaczone
        self.answer_var.set("")  # Odznacz wszystkie - użyj istniejącej zmiennej
        for i, odp in enumerate(question['odpowiedzi']):
            rb = Radiobutton(
                self.frame_answers,
                text=odp,
                variable=self.answer_var,
                value=str(i),
                font=font.Font(size=11),
                bg=COLOR_BG,
                fg=COLOR_DARK,
                activebackground=COLOR_LIGHT,
                selectcolor=COLOR_LIGHT,
                anchor='w',
                wraplength=800,
                padx=10,
                pady=5
            )
            rb.pack(fill='x', padx=5, pady=2)
            self.radio_buttons.append(rb)
        
        # Aktualizuj info
        self.label_info.config(
            text=f"Pytanie {index + 1}/20"
        )
        
        # Aktualizuj scrollowanie i przewiń na górę
        self.frame_question.update_idletasks()
        if hasattr(self, 'test_canvas'):
            self.test_canvas.configure(scrollregion=self.test_canvas.bbox("all"))
            self.test_canvas.yview_moveto(0)
        
        # Aktualizuj scrollowanie
        self.frame_question.update_idletasks()
        if hasattr(self, 'test_canvas'):
            self.test_canvas.configure(scrollregion=self.test_canvas.bbox("all"))
            # Przewiń na górę
            self.test_canvas.yview_moveto(0)
    
    def submit_answer(self):
        """Zatwierdź odpowiedź"""
        selected = self.answer_var.get()
        
        if not selected:
            messagebox.showwarning("Uwaga", "Wybierz odpowiedź!")
            return
        
        question = self.current_test['questions'][self.current_question_index]
        user_choice = int(selected)
        correct_choice = question['prawidlowa']
        
        is_correct = user_choice == correct_choice
        
        # Zapisz odpowiedź
        self.user_answers.append({
            'question_id': question['id'],
            'user_answer': user_choice,
            'correct_answer': correct_choice,
            'is_correct': is_correct
        })
        
        if is_correct:
            self.current_test['correct'] += 1
        
        # Pokaż wynik
        if is_correct:
            self.label_result.config(
                text="✓ Poprawna odpowiedź!",
                fg=COLOR_CORRECT
            )
        else:
            correct_text = question['odpowiedzi'][correct_choice]
            self.label_result.config(
                text=f"✗ Niepoprawna odpowiedź. Prawidłowa: {correct_text}",
                fg=COLOR_INCORRECT
            )
            
            # Pokaż tłumaczenie
            self.text_explanation.config(state='normal')
            self.text_explanation.delete(1.0, 'end')
            self.text_explanation.insert(1.0, f"💡 {question['tlumaczenie']}")
            self.text_explanation.config(state='disabled')
        
        # Podświetl wybrane odpowiedzi
        for i, rb in enumerate(self.radio_buttons):
            if i == user_choice:
                rb.config(fg=COLOR_INCORRECT if not is_correct else COLOR_CORRECT)
            if i == correct_choice and not is_correct:
                rb.config(fg=COLOR_CORRECT, font=font.Font(size=11, weight='bold'))
        
        # Aktualizuj przyciski
        self.btn_submit.config(state='disabled')
        
        # Jeśli to ostatnie pytanie, zmień na "Zakończ test"
        if self.current_question_index == len(self.current_test['questions']) - 1:
            self.btn_next.config(text="🏁 Zakończ test")
        
        self.btn_next.config(state='normal')
    
    def next_question(self):
        """Następne pytanie"""
        self.current_question_index += 1
        
        if self.current_question_index >= len(self.current_test['questions']):
            self.finish_test()
        else:
            self.show_question(self.current_question_index)
            self.btn_submit.config(state='normal')
            
            # Przywróć przycisk
            if self.current_question_index == len(self.current_test['questions']) - 1:
                self.btn_next.config(text="🏁 Zakończ test")
            else:
                self.btn_next.config(text="⏭ Następne pytanie")
                self.btn_next.config(state='disabled')
    
    def finish_test(self):
        """Zakończ test i pokaż wyniki"""
        total = len(self.current_test['questions'])
        correct = self.current_test['correct']
        percentage = (correct / total) * 100
        
        end_time = datetime.datetime.now()
        duration = (end_time - self.test_start_time).total_seconds()
        
        # Zapisz do historii
        test_record = {
            'date': datetime.datetime.now().isoformat(),
            'duration_seconds': int(duration),
            'total': total,
            'correct': correct,
            'percentage': round(percentage, 1),
            'answers': self.user_answers
        }
        
        self.history.insert(0, test_record)  # Dodaj na początek
        self.save_history()
        
        # Pokaż wyniki
        result_text = f"""
Wynik testu:

Prawidłowych odpowiedzi: {correct}/{total}
Procent: {percentage:.1f}%

Czas: {int(duration // 60)} min {int(duration % 60)} sek

        """
        
        if percentage >= 90:
            result_text += "🎉 Doskonały wynik!"
        elif percentage >= 70:
            result_text += "👍 Dobry wynik!"
        elif percentage >= 50:
            result_text += "📚 Warto jeszcze poćwiczyć"
        else:
            result_text += "💪 Nie poddawaj się, powtarzaj materiał!"
        
        messagebox.showinfo("Test zakończony", result_text)
        
        # Reset GUI
        self.reset_test()
        
        # Przejdź do historii
        self.notebook.select(1)
        self.refresh_history()
    
    def reset_test(self):
        """Reset stanu testu"""
        self.current_test = None
        self.current_question_index = 0
        self.user_answers = []
        
        self.text_question.config(state='normal')
        self.text_question.delete(1.0, 'end')
        self.text_question.config(state='disabled')
        
        self.text_code.config(state='normal')
        self.text_code.delete(1.0, 'end')
        self.text_code.config(state='disabled')
        self.code_frame.pack_forget()
        self.code_label.pack_forget()
        
        for rb in self.radio_buttons:
            rb.destroy()
        self.radio_buttons = []
        
        # Odznacz wszystkie radio buttons
        self.answer_var.set("")
        
        self.label_result.config(text="")
        self.text_explanation.config(state='normal')
        self.text_explanation.delete(1.0, 'end')
        self.text_explanation.config(state='disabled')
        
        self.label_info.config(text="Kliknij 'Rozpocznij test' aby rozpocząć")
        
        self.btn_start.config(state='normal')
        self.btn_submit.config(state='disabled')
        self.btn_next.config(state='disabled')
        self.btn_next.config(text="⏭ Następne pytanie")
    
    def refresh_history(self):
        """Odśwież historię testów"""
        self.text_history.config(state='normal')
        self.text_history.delete(1.0, 'end')
        
        if not self.history:
            self.text_history.insert(1.0, "Brak historii testów. Rozpocznij test aby zapisać wynik.")
        else:
            history_text = ""
            for i, test in enumerate(self.history[:20], 1):  # Max 20 ostatnich
                date = datetime.datetime.fromisoformat(test['date'])
                date_str = date.strftime("%Y-%m-%d %H:%M")
                
                duration_min = test['duration_seconds'] // 60
                duration_sec = test['duration_seconds'] % 60
                
                emoji = "🎉" if test['percentage'] >= 90 else "👍" if test['percentage'] >= 70 else "📚"
                
                history_text += f"""
{emoji} Test #{i} - {date_str}
   Wynik: {test['correct']}/{test['total']} ({test['percentage']}%)
   Czas: {duration_min} min {duration_sec} sek
   {'─' * 50}
"""
            
            self.text_history.insert(1.0, history_text.strip())
        
        self.text_history.config(state='disabled')


def main():
    root = Tk()
    app = TestPythonGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

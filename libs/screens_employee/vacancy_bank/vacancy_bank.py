import json
from time import sleep

from kivy.metrics import dp
from kivy.network.urlrequest import UrlRequest
from kivy.properties import get_color_from_hex, ObjectProperty, ListProperty, NumericProperty, Clock
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.divider import MDDivider
from kivymd.uix.chip import MDChip, MDChipText
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty


from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.divider import MDDivider
from kivymd.uix.chip import MDChip, MDChipText
from kivy.properties import StringProperty
from kivymd.uix.snackbar import MDSnackbarText


class OpportunityCard(MDBoxLayout):
    function = StringProperty('')
    city = StringProperty('')
    state = StringProperty('')
    salary = StringProperty('')
    method = StringProperty('Diaria')
    text_chip = StringProperty('Candidatar-se')
    color_divider = StringProperty()
    function_key = StringProperty()
    employee_key = StringProperty()
    request = ObjectProperty()

    def __init__(self, **kwargs):
        # Set explicit sizing
        kwargs['size_hint_y'] = None

        kwargs['height'] = dp(140)  # Increased height for better visibility
        kwargs['size_hint_x'] = 1  # Full width of parent
        kwargs['pos_hint'] = {'center_x': 0.5, 'center_y': 0.5}

        # Process salary
        salary = kwargs.get('salary', '')
        kwargs['salary'] = str(salary).replace('.', ',') if salary is not None else ''

        # Extract and remove custom properties
        self.function = kwargs.pop('function', '')
        self.city = kwargs.pop('city', '')
        self.state = kwargs.pop('state', '')
        self.salary = kwargs.pop('salary', '')
        self.method = kwargs.pop('method', 'Diaria')
        self.text_chip = kwargs.pop('text_chip', 'Candidatar-se')
        self.color_divider = kwargs.pop('color_divider', 'blue')

        # Default card settings
        kwargs.update({
            'theme_bg_color': 'Custom',
            'md_bg_color': (1, 1, 1, 1),
        })

        super().__init__(**kwargs)
        self.build()

    def build(self):
        self.clear_widgets()

        # Main relative layout
        relative = MDRelativeLayout(size_hint=(1, 1))

        # Vertical divider
        divider = MDDivider(
            orientation='vertical',
            size_hint_y=0.75,
            color=self.color_divider,
            divider_width='5dp',
            pos_hint={'center_y': 0.4}
        )

        self.ids['metadinha'] = divider
        # Main content box
        box_all = MDBoxLayout(
            orientation='vertical',
            size_hint=(0.95, 1),
            theme_bg_color='Custom',
            md_bg_color=(1, 1, 1, 1),
            padding=[10, 0, 0, 0],
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            spacing=dp(10)  # Add spacing between sections
        )

        # Function section
        func = MDLabel(
            text=self.function,
            font_style='Title',
            bold=True,
            role='medium',
            size_hint_y=None,
            height=dp(20)
        )

        # Location and Salary section
        loc = MDLabel(
            text=f"Localização: {self.city}, {self.state}",
            font_style='Label',
            role='small',
            size_hint_y=None,
            height=dp(15)
        )
        sal = MDLabel(
            text=f"Valor: R${self.salary}",
            font_style='Label',
            role='small',
            size_hint_y=None,
            height=dp(15)
        )

        # Payment and Chip section
        relative_two = MDRelativeLayout(size_hint_y=None, height=dp(30))
        met = MDLabel(
            text=f"Pagamento: {self.method}",
            halign='left',
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_style='Label',
            role='small'
        )

        chip_text = MDChipText(
                text=self.text_chip,
                theme_text_color='Custom',
                text_color='white',
                font_style='Label',
                role='medium',
                bold=True
        )
        self.ids['text_chip'] = chip_text
        chip = MDChip(
            chip_text,
            type="input",
            theme_bg_color='Custom',
            theme_line_color='Custom',
            line_color=get_color_from_hex('#7692FF'),
            md_bg_color=self.color_divider,
            _no_ripple_effect=True,
            pos_hint={'center_y': 0.5, 'center_x': 0.8}
        )
        self.ids['chip'] = chip
        chip.bind(
            on_release=lambda instance, key=self.function_key: self.add_key(key)
        )

        # Assemble components
        relative_two.add_widget(met)
        relative_two.add_widget(chip)

        # Add all sections to main box
        box_all.add_widget(func)
        box_all.add_widget(loc)
        box_all.add_widget(sal)
        box_all.add_widget(relative_two)

        relative.add_widget(divider)
        relative.add_widget(box_all)
        self.add_widget(relative)

    def add_key(self, key):
        if self.text_chip not in 'Submetido':
            # adicionar a key ao requests do mesmo
            new_request = self.request
            new_request.append(self.employee_key)
            data = {
                'requests': f"{new_request}"
            }

            UrlRequest(
                url=f'https://obra-7ebd9-default-rtdb.firebaseio.com/Functions/{key}/.json',
                method='PATCH',
                req_body=json.dumps(data),
                on_success=self.sucefful
            )

    def sucefful(self, instance, result):
        self.ids.chip.md_bg_color = 'green'
        self.ids.metadinha.color = 'green'
        self.ids.text_chip.text = 'Submetido'


class VacancyBank(MDScreen):
    current_nav_state = StringProperty('vacancy')
    add = True
    type = ''
    key = StringProperty()
    avatar = StringProperty()
    employee_name = StringProperty()
    employee_function = StringProperty()
    employee_mail = StringProperty()
    employee_telephone = StringProperty()
    employee_summary = StringProperty()
    skills = StringProperty()
    number = 0

    # Lista para armazenar todos os dados
    all_functions = ListProperty([])

    # Controle de paginação
    current_page = NumericProperty(0)
    items_per_page = NumericProperty(3)

    # Tracking loaded function keys to prevent duplicates
    loaded_function_keys = ListProperty([])

    def on_enter(self, *args):
        print(self.key)
        # Limpa qualquer conteúdo anterior
        self.type = 'loc'
        self.ids.main_scroll.clear_widgets()
        self.ids.vacancy.active = True
        # Redefine a paginação
        self.current_page = 0
        self.all_functions = []
        self.loaded_function_keys = []  # Reset loaded keys

        # Carrega funções do Firebase
        self.load_functions()

    def load_functions(self):
        url = f"https://obra-7ebd9-default-rtdb.firebaseio.com/Functions/.json"
        UrlRequest(
            url,
            on_success=self.prepare_functions
        )

    def prepare_functions(self, instance, result):
        # Filtra e organiza as funções
        filtered_functions = []
        for key, item in result.items():
            requests = eval(item['requests'])

            # Só adiciona funções onde o usuário não se candidatou
            if self.key not in requests:
                function_data = {
                    'key': key,
                    'requests': requests,
                    'occupation': item['occupation'],
                    'City': item['City'],
                    'State': item['State'],
                    'Salary': item['Salary'],
                    'Option Payment': item['Option Payment'],
                    
                }
                filtered_functions.append(function_data)

        # Atualiza a lista de funções
        self.all_functions = filtered_functions

        # Carrega os primeiros cards
        self.load_more_functions()

    def load_more_functions(self):
        # Calcula o índice de início e fim
        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page

        # Verifica se ainda há itens para carregar
        if start_index >= len(self.all_functions):
            return False

        # Carrega cards para a página atual
        for item in self.all_functions[start_index:end_index]:
            # Check if this function key has already been loaded
            if item['key'] not in self.loaded_function_keys:
                card = OpportunityCard(
                    function=item['occupation'],
                    city=item['City'],
                    state=item['State'],
                    salary=item['Salary'],
                    method=item['Option Payment'],
                    text_chip='Candidatar-se',
                    color_divider='blue',
                    function_key=item['key'],
                    employee_key=self.key,
                    request=item['requests']
                )
                self.ids.main_scroll.add_widget(card)

                # Add the key to loaded keys to prevent duplicates
                self.loaded_function_keys.append(item['key'])
            else:
                card = OpportunityCard(
                    function=item['occupation'],
                    city=item['City'],
                    state=item['State'],
                    salary=item['Salary'],
                    method=item['Option Payment'],
                    text_chip='Submetido',
                    color_divider='green',
                    function_key=item['key'],
                    employee_key=self.key,
                    request=item['requests']
                )
                self.ids.main_scroll.add_widget(card)

                # Add the key to loaded keys to prevent duplicates
                self.loaded_function_keys.append(item['key'])

        # Incrementa o número da página
        self.current_page += 1
        return True

    def on_size(self, *args):
        # Método para carregar mais cards quando o layout é pequeno
        scroll_view = self.ids.main_scroll.parent

        # Verifica se o conteúdo é menor que a altura da scroll view
        if (self.ids.main_scroll.height <= scroll_view.height and
                self.current_page * self.items_per_page < len(self.all_functions)):
            self.load_more_functions()

    def check_scroll(self, scroll_view, *args):
        # Verifica se está no final do scroll
        if self.add:
            if scroll_view.scroll_y <= 0:
                # Tenta carregar mais cards
                more_items = self.load_more_functions()

                # Se não há mais itens, volta o scroll para o topo
                if not more_items:
                    print('Acabaram os widgets')

    def search(self, instance, text):
        self.add = False
        # Normalize search text
        self.text_search = text.strip().lower()

        # Validate search input
        if not self.text_search:
            self.show_no_input_warning()
            return

        # Clear previous results
        self.ids.main_scroll.clear_widgets()

        # Perform search
        self.number += 1
        if self.number == 2:
            self.perform_search()
            self.number = 0

    def perform_search(self):
        url = f"https://obra-7ebd9-default-rtdb.firebaseio.com/Functions/.json"

        # Show loading indicator
        self.show_loading_indicator()

        UrlRequest(
            url,
            on_success=self.analyze_search_results,
        )

    def analyze_search_results(self, instance, data):
        # Hide loading indicator
        self.hide_loading_indicator()

        # Store matched results
        matched_results = []

        for key, item in data.items():
            # Check if search matches location or function based on current type
            if self.type == 'loc':
                match_condition = (
                        self.text_search in item['City'].lower() or
                        self.text_search in item['State'].lower()
                )
            elif self.type == 'func':
                match_condition = (
                        self.text_search in item['occupation'].lower()
                )
            else:
                match_condition = False

            # Process matched items
            if match_condition:
                requests = eval(item['requests'])

                # Determine chip text and color based on request status
                if self.key not in requests:
                    chip_text = 'Candidatar-se'
                    divider_color = 'blue'
                else:
                    chip_text = 'Submetido'
                    divider_color = 'green'

                # Create opportunity card
                card = OpportunityCard(
                    function=item['occupation'],
                    city=item['City'],
                    state=item['State'],
                    salary=item['Salary'],
                    method=item['Option Payment'],
                    text_chip=chip_text,
                    color_divider=divider_color
                )

                matched_results.append(card)

        # Handle search results
        if matched_results:
            # Add matched cards to scroll view
            for card in matched_results:
                self.ids.main_scroll.add_widget(card)


            # Optional: Scroll to top of results
            self.scroll_to_top()
        else:
            # Show no results found message
            self.show_no_results_message()

    def show_loading_indicator(self):
        # Create and show a loading spinner or message
        loading_label = MDLabel(
            text="\nBuscando...",
            halign="center",
            theme_text_color="Secondary"
        )
        self.ids.main_scroll.clear_widgets()
        self.ids.main_scroll.add_widget(loading_label)

    def hide_loading_indicator(self):
        # Clear loading indicator
        self.ids.main_scroll.clear_widgets()

    def show_no_results_message(self):
        # Display a user-friendly "no results" message
        no_results_label = MDLabel(
            text="\nTente outro termo de busca.",
            halign="center",
            theme_text_color="Secondary",
            font_style="Title"
        )
        self.add = True
        self.ids.main_scroll.add_widget(no_results_label)


    def show_no_input_warning(self):
        # Show a warning if no search input is provided
        from kivymd.uix.snackbar import MDSnackbar

        MDSnackbar(
            MDSnackbarText(
                text='Coloque um termo para a busca',
                theme_text_color='Custom',
                text_color='white',
                bold=True
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            halign='center',
            size_hint_x=0.8,
            theme_bg_color='Custom',
            background_color=get_color_from_hex('#2F6690')
        ).open()

    def scroll_to_top(self):
        # Scroll to the top of the results (if scroll view supports it)
        try:
            self.ids.main_scroll.parent.scroll_y = 1
        except Exception:
            pass

    def add_search_results(self, matched_results):
        # Add matched cards to scroll view
        for card in matched_results:
            self.ids.main_scroll.add_widget(card)

    def loc(self):
        self.type = 'loc'
        self.ids.hint.text = 'Buscar por localização'
        self.ids.tp.focus = True
        self.ids.loc_text.text_color = 'white'
        self.ids.loc.md_bg_color = get_color_from_hex('#7692FF')

        self.ids.func.md_bg_color = 'white'
        self.ids.func.line_color = get_color_from_hex('#7692FF')
        self.ids.func_text.text_color = get_color_from_hex('#7692FF')
        self.ids.tp.text = ''

    def func(self):
        self.type = 'func'
        self.ids.hint.text = 'Buscar por função'
        self.ids.tp.focus = True
        self.ids.func.md_bg_color = get_color_from_hex('#7692FF')
        self.ids.func_text.text_color = 'white'

        self.ids.loc.md_bg_color = 'white'
        self.ids.loc.line_color = get_color_from_hex('#7692FF')
        self.ids.loc_text.text_color = get_color_from_hex('#7692FF')
        self.ids.tp.text = ''

    def perfil(self):
        """
        Navega para a tela de perfil e ajusta o estado global de navegação
        """
        app = MDApp.get_running_app()
        screenmanager = app.root

        # Obtém a tela de perfil
        perfil = screenmanager.get_screen('PrincipalScreenEmployee')

        # Transfere os dados do usuário
        perfil.key = self.key
        perfil.employee_name = self.employee_name
        perfil.employee_function = self.employee_function
        perfil.employee_mail = self.employee_mail
        perfil.employee_telephone = self.employee_telephone
        perfil.avatar = self.avatar
        perfil.employee_summary = self.employee_summary
        perfil.skills = self.skills

        # Define o estado de navegação global
        perfil.current_nav_state = 'perfil'

        # Navega para a tela de perfil
        screenmanager.transition = SlideTransition(direction='right')
        screenmanager.current = 'PrincipalScreenEmployee'


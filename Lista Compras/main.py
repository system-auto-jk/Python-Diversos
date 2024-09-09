from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import openpyxl

# Configura o tamanho da janela para simular a tela de um celular
Window.size = (360, 640)

# Simula um banco de dados para armazenar produtos
produtos = {
    'ASSAÍ': [],
    'Lista 2': [],
    'Lista 3': []
}

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        # Define o background verde usando canvas
        with self.canvas.before:
            Color(255, 99, 71, 0.1)  # Cor verde em RGBA (Red, Green, Blue, Alpha)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Atualiza o tamanho e a posição do retângulo quando a tela muda de tamanho
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = FloatLayout()

        layout.add_widget(Label(text='Bem-vindo(a)', size_hint_y=1.5, font_size=80))

        # Botão para Criar Lista
        btn_create_list = Button(text="Criar Lista", font_size = 50,size_hint=(.8, .1), pos_hint={'x': .1, 'y': .25})
        btn_create_list.background_color = (0.2, 0.8, 0.2, 1)  # Verde
        btn_create_list.background_normal = ''
        btn_create_list.bind(on_press=self.go_to_create_list)

        # Botão para Ver Lista
        btn_view_list = Button(text="Ver Lista", font_size = 50, size_hint=(.8, .1), pos_hint={'x': .1, 'y': .1})
        btn_view_list.background_color = ('#FE556A')  # Verde
        btn_view_list.background_normal = ''
        btn_view_list.bind(on_press=self.go_to_view_list)

        layout.add_widget(btn_create_list)
        layout.add_widget(btn_view_list)

        self.add_widget(layout)

    def _update_rect(self, *args):
        """Atualiza o retângulo de fundo ao redimensionar a tela."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def go_to_create_list(self, instance):
        self.manager.current = 'create_list'

    def go_to_view_list(self, instance):
        self.manager.current = 'view_list'

class CreateListScreen(Screen):
    def __init__(self, **kwargs):
        super(CreateListScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Spinner para selecionar a lista predefinida
        self.spinner = Spinner(
            text='Escolha uma lista',
            values=('ASSAÍ', 'Lista 2', 'Lista 3'),
            size_hint=(1, .08),
            pos_hint={'y': .4},
            font_size=40
        )

        # Adicione os campos de entrada para o formulário
        self.product_input = TextInput(hint_text='Produto', size_hint_y=0.12, font_size=70)
        self.quantity_input = TextInput(hint_text='Quantidade', size_hint_y=0.12, font_size=70)
        self.brand_input = TextInput(hint_text='Marca', size_hint_y=0.12, font_size=70)
        self.value_input = TextInput(hint_text='Valor', size_hint_y=0.12, font_size=70)

        layout.add_widget(Label(text='Adicionar Novo Produto', size_hint_y=0.12, font_size=70, bold=True))
        layout.add_widget(self.spinner)
        layout.add_widget(self.product_input)
        layout.add_widget(self.quantity_input)
        layout.add_widget(self.brand_input)
        layout.add_widget(self.value_input)

        # Botão para salvar as informações
        btn_save = Button(text="Salvar", size_hint_y=0.12, font_size=50)
        btn_save.background_color = (0.2, 0.8, 0.2, 1)  # Verde
        btn_save.background_normal = ''
        btn_save.bind(on_press=self.confirm_save_product)

        # Botão para voltar
        btn_back = Button(text="Voltar", size_hint_y=0.12, font_size=50)
        btn_back.background_color = ('#FEDD59')  # Vermelho
        btn_back.color = 'white'
        btn_back.background_normal = ''
        btn_back.bind(on_press=self.go_back)

        layout.add_widget(btn_save)
        layout.add_widget(btn_back)

        self.add_widget(layout)
    
    def confirm_save_product(self, instance):
        # Verifica se uma lista foi selecionada
        if self.spinner.text == 'Escolha uma lista':
            self.show_warning_popup("Por favor, selecione uma lista antes de salvar.")
            return

        # Cria e exibe um popup de confirmação
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text='Deseja realmente salvar o produto?')
        btn_confirm = Button(text='Confirmar', size_hint_y=None, font_size=50)
        btn_confirm.background_color = (0.2, 0.8, 0.2, 1)  # Verde
        btn_confirm.background_normal = ''
        btn_confirm.bind(on_press=self.save_product)

        btn_cancel = Button(text='Cancelar', size_hint_y=None, font_size=50)
        btn_cancel.background_color = (1, 0, 0, 1)  # Vermelho
        btn_cancel.background_normal = ''
        btn_cancel.bind(on_press=self.dismiss_popup)

        content.add_widget(label)
        content.add_widget(btn_confirm)
        content.add_widget(btn_cancel)

        self.popup = Popup(title='Confirmar', content=content, size_hint=(.8, .4))
        self.popup.open()
    
    def save_product(self, instance):
        self.lista_selecionada = self.spinner.text
        produto = self.product_input.text
        quantidade = self.quantity_input.text
        marca = self.brand_input.text
        valor = self.value_input.text
        
        # Adiciona o produto à lista selecionada
        produtos[self.lista_selecionada].append({
            'Produto': produto,
            'Quantidade': quantidade,
            'Marca': marca,
            'Valor': valor
        })
        
        print(f'Lista: {self.lista_selecionada}, Produto: {produto}, Quantidade: {quantidade}, Marca: {marca}, Valor: {valor}')
        
        # Limpar campos após salvar
        self.product_input.text = ''
        self.quantity_input.text = ''
        self.brand_input.text = ''
        self.value_input.text = ''
        
        # Fechar o popup
        self.dismiss_popup()
        
        # Manter a tela atual para adicionar mais produtos
        self.manager.current = 'create_list'
    
    def dismiss_popup(self, instance=None):
        # Fechar o popup
        if hasattr(self, 'popup'):
            self.popup.dismiss()
    def show_warning_popup(self, message):
        # Exibe um popup de aviso
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text=message)
        btn_close = Button(text='Fechar', size_hint_y=None, height=50)
        btn_close.bind(on_press=self.dismiss_popup)

        content.add_widget(label)
        content.add_widget(btn_close)

        self.popup = Popup(title='Aviso', content=content, size_hint=(.8, .4))
        self.popup.open()
    
    def go_back(self, instance):
        self.manager.current = 'home'
class ViewListScreen(Screen):
    def __init__(self, **kwargs):
        super(ViewListScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.spinner = Spinner(
            text='Escolha uma lista',
            values=('ASSAÍ', 'Lista 2', 'Lista 3'),
            size_hint=(1, .08),
            pos_hint={'y': .4},
            font_size=40
        )
        self.spinner.bind(text=self.update_product_list)

        # Layout para a tabela
        self.grid_layout = GridLayout(cols=6, size_hint_y=None, spacing=10, row_default_height=40)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, .9), do_scroll_x=True, do_scroll_y=True)
        scroll_view.add_widget(self.grid_layout)

        self.total_label = Label(text='Total: R$ 0.00', size_hint_y=None, height=40)
        self.purchased_label = Label(text='Valor a Pagar: R$ 0.00', size_hint_y=None, height=40)

        layout.add_widget(Label(text='Visualizar Produtos', size_hint_y=0.12, font_size=70, bold=True))
        layout.add_widget(self.spinner)
        layout.add_widget(scroll_view)
        layout.add_widget(self.total_label)
        layout.add_widget(self.purchased_label)

        btn_excel = Button(text="Exportar Excel", size_hint_y=0.12, font_size=50)
        btn_excel.background_color = ('#FEDD59')  # Vermelho
        btn_excel.background_normal = ''
        btn_excel.bind(on_press=self.export_to_excel)

        layout.add_widget(btn_excel)

        btn_back = Button(text="Voltar", size_hint_y=0.12, font_size=50)
        btn_back.background_color = ('#FEDD59')  # Vermelho
        btn_back.background_normal = ''
        btn_back.bind(on_press=self.go_back)

        layout.add_widget(btn_back)


        self.add_widget(layout)

    def export_to_excel(self, instance):
        
        book = openpyxl.Workbook()
        pagina = book['Sheet']
        pagina.append(['Produto','Quantidade','Marca','Valor'])

        for i in self.lista_toda:
            print(i.split())
            pagina.append(i.split())

        
        book.save(f'{self.spinner.text}.xlsx')

    def update_product_list(self, spinner, text):
        self.lista_toda = []
        self.grid_layout.clear_widgets()

        # Cabeçalhos
        self.grid_layout.add_widget(Label(text='ID', bold=True))
        self.grid_layout.add_widget(Label(text='Produto', bold=True))
        self.grid_layout.add_widget(Label(text='Qntd', bold=True))
        self.grid_layout.add_widget(Label(text='Marca', bold=True))
        self.grid_layout.add_widget(Label(text='Valor Uni.', bold=True))
        self.grid_layout.add_widget(Label(text='Ações', bold=True))

        total_value = 0.0
        purchased_value = 0.0

        for i, produto in enumerate(produtos.get(text, [])):
            # ID do Produto
            self.grid_layout.add_widget(Label(text=str(i + 1)))

            # Dados do Produto
            color = (1, 1, 1, 1)  # Branco
            if produto.get('Comprado'):
                color = (0, 1, 0, 1)  # Verde

            self.grid_layout.add_widget(Label(text=produto['Produto'], color=color))
            self.grid_layout.add_widget(Label(text=str(produto['Quantidade']), color=color))
            self.grid_layout.add_widget(Label(text=produto['Marca'], color=color))
            self.grid_layout.add_widget(Label(text=produto['Valor'], color=color))
            self.lista_toda.append(f"{produto['Produto']} {produto['Quantidade']} {produto['Marca']} {produto['Valor']}\n")
            


            # Cálculo do valor total do produto
            try:
                quantidade = float(produto['Quantidade'])
                valor_unitario = float(produto['Valor'].replace('R$', '').replace(',', '.'))
                valor_total_produto = quantidade * valor_unitario
            except ValueError:
                valor_total_produto = 0.0

            # Atualizar totais
            if produto.get('Comprado'):
                purchased_value += valor_total_produto
            else:
                total_value += valor_total_produto

            # Ações
            btn_add_to_cart = Button(text='C', size_hint=(None, None), size=(80, 50), font_size=50, bold=True)
            btn_add_to_cart.bind(on_press=lambda btn, idx=i: self.confirm_mark_as_bought(idx))

            btn_edit = Button(text="E", size_hint=(None, None), size=(70, 50))
            btn_edit.bind(on_press=lambda btn, idx=i: self.edit_product(idx))

            btn_delete = Button(text="X", size_hint=(None, None), size=(40, 50))
            btn_delete.bind(on_press=lambda btn, idx=i: self.confirm_delete_product(idx))

            actions_box = BoxLayout(orientation='horizontal', spacing=5, size_hint_x=None, width=120)
            actions_box.add_widget(btn_add_to_cart)
            actions_box.add_widget(btn_edit)
            actions_box.add_widget(btn_delete)

            self.grid_layout.add_widget(actions_box)

        self.total_label.text = f'Total: R$ {total_value:.2f}'
        self.purchased_label.text = f'Valor a Pagar: R$ {purchased_value:.2f}'


    
    def confirm_mark_as_bought(self, index):
        lista = self.spinner.text
        if index < len(produtos[lista]):
            produto = produtos[lista][index]
            
            # Verifica se o produto já está marcado como comprado
            if produto.get('Comprado'):
                mensagem = f'Deseja desmarcar "{produto["Produto"]}" como comprado?'
                acao_confirmacao = lambda btn: self.unmark_as_bought(index)
            else:
                mensagem = f'Deseja marcar "{produto["Produto"]}" como comprado?'
                acao_confirmacao = lambda btn: self.mark_as_bought(index)

            # Criação do popup de confirmação
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            content.add_widget(Label(text=mensagem))
            
            btn_confirm = Button(text="Confirmar", size_hint_y=None, height=50)
            btn_confirm.background_color = (0, 1, 0, 1)  # Verde
            btn_confirm.background_normal = ''
            btn_confirm.bind(on_press=acao_confirmacao)
            
            btn_cancel = Button(text="Cancelar", size_hint_y=None, height=50)
            btn_cancel.background_color = (1, 0, 0, 1)  # Vermelho
            btn_cancel.background_normal = ''
            btn_cancel.bind(on_press=self.close_popup)
            
            content.add_widget(btn_confirm)
            content.add_widget(btn_cancel)
            
            self.popup = Popup(title='Confirmar Ação', content=content, size_hint=(0.8, 0.4))
            self.popup.open()

    def mark_as_bought(self, index):
        lista = self.spinner.text
        if index < len(produtos[lista]):
            produto = produtos[lista][index]
            produto['Comprado'] = True  # Marca como comprado
            self.update_product_list(self.spinner, lista)
        self.close_popup(None)

    def unmark_as_bought(self, index):
        lista = self.spinner.text
        if index < len(produtos[lista]):
            produto = produtos[lista][index]
            produto['Comprado'] = False  # Desmarca como comprado
            self.update_product_list(self.spinner, lista)
        self.close_popup(None)


    
    def edit_product(self, index):
        self.manager.current = 'edit_product'
        self.manager.get_screen('edit_product').set_product(index, self.spinner.text)

    def confirm_delete_product(self, index):
        # Create a confirmation popup
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Você tem certeza que deseja excluir este produto?'))
        
        btn_confirm = Button(text="Excluir", size_hint_y=None, height=50)
        btn_confirm.background_color = (1, 0, 0, 1)  # Vermelho
        btn_confirm.background_normal = ''
        btn_confirm.bind(on_press=lambda btn: self.delete_product(index))
        
        btn_cancel = Button(text="Cancelar", size_hint_y=None, height=50)
        btn_cancel.background_color = (0, 1, 0, 1)  # Verde
        btn_cancel.background_normal = ''
        btn_cancel.bind(on_press=self.close_popup)
        
        content.add_widget(btn_confirm)
        content.add_widget(btn_cancel)
        
        self.popup = Popup(title='Confirmar Exclusão', content=content, size_hint=(0.8, 0.4))
        self.popup.open()

    def delete_product(self, index):
        lista = self.spinner.text
        if index < len(produtos[lista]):
            del produtos[lista][index]
            self.update_product_list(self.spinner, lista)
        self.close_popup(None)

    def close_popup(self, instance):
        if hasattr(self, 'popup'):
            self.popup.dismiss()
    
    def go_back(self, instance):
        self.manager.current = 'home'

class EditProductScreen(Screen):
    def __init__(self, **kwargs):
        super(EditProductScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Campos de entrada para edição do produto
        self.product_input = TextInput(hint_text='Produto', size_hint_y=0.12,font_size=70)
        self.quantity_input = TextInput(hint_text='Quantidade', size_hint_y=0.12, font_size=70)
        self.brand_input = TextInput(hint_text='Marca', size_hint_y=0.12, font_size=70)
        self.value_input = TextInput(hint_text='Valor', size_hint_y=0.12, font_size=70)
        
        layout.add_widget(Label(text='Editar Produto', font_size=70, size_hint_y=None))
        layout.add_widget(self.product_input)
        layout.add_widget(self.quantity_input)
        layout.add_widget(self.brand_input)
        layout.add_widget(self.value_input)
        
        # Botão para salvar as alterações
        btn_save = Button(text="Salvar", size_hint_y=0.12, font_size=50)
        btn_save.background_color = (0.2, 0.8, 0.2, 1)  # Verde
        btn_save.background_normal = ''
        btn_save.bind(on_press=self.confirm_save_product)
        
        # Botão para voltar
        btn_back = Button(text="Voltar", size_hint_y=0.12, font_size=50)
        btn_back.background_color = ('#FEDD59')  # Vermelho
        btn_back.background_normal = ''
        btn_back.bind(on_press=self.go_back)
        
        layout.add_widget(btn_save)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def set_product(self, index, lista):
        self.index = index
        self.lista = lista
        produto = produtos[lista][index]
        self.product_input.text = produto['Produto']
        self.quantity_input.text = produto['Quantidade']
        self.brand_input.text = produto['Marca']
        self.value_input.text = produto['Valor']
    
    def confirm_save_product(self, instance):
        # Cria e exibe um popup de confirmação
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(text='Deseja realmente salvar as alterações?')
        btn_confirm = Button(text='Confirmar', size_hint_y=None, font_size=50)
        btn_confirm.background_color = (0.2, 0.8, 0.2, 1)  # Verde
        btn_confirm.background_normal = ''
        btn_confirm.bind(on_press=self.save_product)
        
        btn_cancel = Button(text='Cancelar', size_hint_y=None, font_size=50)
        btn_cancel.background_color = (1, 0, 0, 1)  # Vermelho
        btn_cancel.background_normal = ''
        btn_cancel.bind(on_press=self.dismiss_popup)
    
        content.add_widget(label)
        content.add_widget(btn_confirm)
        content.add_widget(btn_cancel)
        
        self.popup = Popup(title='Confirmar', content=content, size_hint=(.8, .4))
        self.popup.open()
    
    def save_product(self, instance):
        produto = self.product_input.text
        quantidade = self.quantity_input.text
        marca = self.brand_input.text
        valor = self.value_input.text
        
        produtos[self.lista][self.index] = {
            'Produto': produto,
            'Quantidade': quantidade,
            'Marca': marca,
            'Valor': valor
        }
        
        self.dismiss_popup()  # Fecha o popup após salvar
        self.manager.get_screen('view_list').update_product_list(self.manager.get_screen('view_list').spinner, self.lista)
        self.manager.current = 'view_list'
    
    def dismiss_popup(self, instance=None):
        # Fechar o popup
        self.popup.dismiss()
    
    def go_back(self, instance):
        self.manager.current = 'view_list'


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CreateListScreen(name='create_list'))
        sm.add_widget(ViewListScreen(name='view_list'))
        sm.add_widget(EditProductScreen(name='edit_product'))
        return sm

if __name__ == '__main__':
    MainApp().run()

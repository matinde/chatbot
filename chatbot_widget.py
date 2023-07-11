#import the flet module
import flet as ft

#import openai
import openai

from config import OPENAI_API_KEY

# call the OpenAI API 
openai.api_key = OPENAI_API_KEY

class Chat(ft.UserControl):

    def build(self):
        #heading
        self.heading = ft.Text(value="ChatGPT Chatbot", size=24)
        self.text_input = ft.TextField(hint_text="Enter your prompt", expand=True, multiline=True)
        self.output_column = ft.Column()
        
        self.scroll=True
        
        # The coloumn dictates how elements will be placed in the layout
        return ft.Column(
            width=800,
            # with controls, you can list the elements. We start with the heading and row and output column.
            controls=[
                self.heading,
                ft.Row(
                    controls=[
                        self.text_input,
                        ft.ElevatedButton("Submit", height=60, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=1)), on_click=self.btn_clicked),
                    ],
                ),
                self.output_column,
            ],
        )
    
    def btn_clicked(self, event):

        # Send the input text to the ChatGPT API
        completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[
                    {"role": "system", "content": "You are useful assistant"},
                    {"role": "user", "content": self.text_input.value},
                ]
            )

        # Get the output text from the API response
        self.output = completion.choices[0].message.content
        
        result = Output(self.output, self.text_input.value, self.outputDelete)
        self.output_column.controls.append(result)
        self.text_input.value = "" # clear the text field
        self.update() # update the page

    def outputDelete(self, result):
        self.output_column.controls.remove(result)
        self.update()


class Output(ft.UserControl):
    def __init__(self, myoutput, mytext_input, myoutput_delete):
        super().__init__()
        self.myoutput = myoutput 
        self.mytext_input = mytext_input
        self.myoutput_delete = myoutput_delete

    def build(self):
        self.output_display = ft.Text(value=self.myoutput, selectable=True)
        self.delete_button = ft.IconButton(ft.icons.DELETE_OUTLINE_SHARP, on_click=self.delete)
        self.input_display = ft.Container(ft.Text(value=self.mytext_input), bgcolor=ft.colors.BLUE_GREY_100, padding=10)
        

        self.display_view = ft.Column(controls=[self.input_display, self.output_display, self.delete_button])

        return self.display_view

    def delete(self, e):
        self.myoutput_delete(self)


def main(page):
    page.scroll = True
    page.window_width = 500
    page.window_height = 700
    mychat = Chat() # create a new object
    page.add(mychat)# add application's root control to the page


ft.app(target=main)
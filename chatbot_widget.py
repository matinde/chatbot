# Import the flet module
import flet as ft

# Import the OpenAI library
import openai

# Import the OpenAI API key from the config file
from config import OPENAI_API_KEY

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Define a class called Chat that is a subclass of ft.UserControl
class Chat(ft.UserControl):

    def build(self):
        # Create a heading text element
        self.heading = ft.Text(value="ChatGPT Chatbot", size=24)
        
        # Create a text input field for user prompts
        self.text_input = ft.TextField(hint_text="Enter your prompt", expand=True, multiline=True)
        
        # Create an empty column to hold the output elements
        self.output_column = ft.Column()
        
        # Enable scrolling in the chat interface
        self.scroll = True
        
        # Create the layout of the chat interface using the ft.Column container
        return ft.Column(
            width=800,
            controls=[
                # Add the heading, text input, and submit button in a row
                self.heading,
                ft.Row(
                    controls=[
                        self.text_input,
                        ft.ElevatedButton("Submit", height=60, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=1)), on_click=self.btn_clicked),
                    ],
                ),
                # Add the output column to display the chatbot responses
                self.output_column,
            ],
        )
    
    def btn_clicked(self, event):
        # Send the user input to the ChatGPT API for completion
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are useful assistant"},
                {"role": "user", "content": self.text_input.value},
            ]
        )

        # Get the output text from the API response
        self.output = completion.choices[0].message.content
        
        # Create a new Output object to display the chatbot response
        result = Output(self.output, self.text_input.value, self.outputDelete)
        
        # Add the Output object to the output column
        self.output_column.controls.append(result)
        
        # Clear the text input field
        self.text_input.value = ""
        
        # Update the page to reflect the changes
        self.update()

    def outputDelete(self, result):
        # Remove the specified result from the output column
        self.output_column.controls.remove(result)
        
        # Update the page to reflect the changes
        self.update()


# Define a class called Output that is a subclass of ft.UserControl
class Output(ft.UserControl):
    def __init__(self, myoutput, mytext_input, myoutput_delete):
        super().__init__()
        self.myoutput = myoutput 
        self.mytext_input = mytext_input
        self.myoutput_delete = myoutput_delete

    def build(self):
        # Create a text element to display the chatbot response
        self.output_display = ft.Text(value=self.myoutput, selectable=True)
        
        # Create a delete button to remove the chatbot response
        self.delete_button = ft.IconButton(ft.icons.DELETE_OUTLINE_SHARP, on_click=self.delete)
        
        # Create a container to display the user input
        self.input_display = ft.Container(ft.Text(value=self.mytext_input), bgcolor=ft.colors.BLUE_GREY_100, padding=10)
        
        # Create a column layout to arrange the elements
        self.display_view = ft.Column(controls=[self.input_display, self.output_display, self.delete_button])

        # Return the column layout as the UI representation of the Output class
        return self.display_view

    def delete(self, e):
        # Call the outputDelete function with the current instance as an argument
        self.myoutput_delete(self)


# Define a main function that sets up the page layout
def main(page):
    page.scroll = True
    page.window_width = 500
    page.window_height = 700
    
    # Create a new Chat object
    mychat = Chat()
    
    # Add the Chat object to the page
    page.add(mychat)


# Run the application using the ft.app() function and pass the main function as the target
ft.app(target=main)

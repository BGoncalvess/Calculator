import flet as ft
import ButtonEvents as be

class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        be.ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        be.ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        be.ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        be.ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        be.DigitButton(text="7", button_clicked=self.button_clicked),
                        be.DigitButton(text="8", button_clicked=self.button_clicked),
                        be.DigitButton(text="9", button_clicked=self.button_clicked),
                        be.ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        be.DigitButton(text="4", button_clicked=self.button_clicked),
                        be.DigitButton(text="5", button_clicked=self.button_clicked),
                        be.DigitButton(text="6", button_clicked=self.button_clicked),
                        be.ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        be.DigitButton(text="1", button_clicked=self.button_clicked),
                        be.DigitButton(text="2", button_clicked=self.button_clicked),
                        be.DigitButton(text="3", button_clicked=self.button_clicked),
                        be.ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        be.DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        be.DigitButton(text=".", button_clicked=self.button_clicked),
                        be.ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data in ("="):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data in ("%"):
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data in ("+/-"):
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            result = self.format_number(operand1 + operand2)

        elif operator == "-":
            result = self.format_number(operand1 - operand2)

        elif operator == "*":
            result = self.format_number(operand1 * operand2)

        elif operator == "/":
            if operand2 == 0:
                result = "Error"
            else:
                result = self.format_number(operand1 / operand2)

        print(f"Calculation result: {result}")
        return result

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True
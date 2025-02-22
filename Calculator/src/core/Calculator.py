import flet as ft
import sympy as sympy
from buttons.DigitButton import DigitButton
from buttons.ExtraActionButton import ExtraActionButton
from buttons.ActionButton import ActionButton
from exceptions.InvalidExpressionException import InvalidExpressionException
from logger.LogFormat import LogFormat

class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.logger = LogFormat(__name__).logger
        self.reset()

        self.expression = ft.Text(value="", color=ft.colors.WHITE, size=16)
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.expression], alignment="end"),
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.expression.value = ""
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0":
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = str(self.result.value) + data
                self.expression.value = self.result.value

        elif data in ("+", "-", "*", "/"):
            self.result.value = str(self.result.value) + data
            self.expression.value = self.result.value
            if self.result.value == "Error":
                self.operand1 = "0"
            self.reset()

        elif data in ("="):
            self.result.value = self.calculate(self.expression.value)
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

    def calculate(self, expression):
        try:
            sympy_expression = sympy.sympify(expression).evalf()
            result = round(float(sympy_expression), 2)
        except sympy.SympifyError as e:
            e = InvalidExpressionException(f"Invalid expression: {expression}", self.logger)
            e.error()
            result = "Error"
            self.expression.value = "Error"

        except ZeroDivisionError as e:
            e = InvalidExpressionException("Division by zero", self.logger)
            e.error()
            result = "Error"
            self.expression.value = "Error"

        self.logger.info(str(result))
        return result

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True

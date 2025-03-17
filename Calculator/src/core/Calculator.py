import flet as ft
import sympy as sympy
from buttons.ActionButton import ActionButton
from buttons.DigitButton import DigitButton
from buttons.ExtraActionButton import ExtraActionButton
from buttons.HistoryButton import HistoryButton
from exceptions.InvalidExpressionException import InvalidExpressionException
from formats.LogFormat import LogFormat
from storage.HistoryStorage import HistoryStorage
from views.HistoryView import HistoryView

class Calculator(ft.Container):
    def __init__(self):
        super().__init__()
        self.logger = LogFormat(__name__).logger
        self.expression = ft.Text(value="", color=ft.colors.WHITE, size=16)
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.history_view = HistoryView()
        self.storage = HistoryStorage
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        HistoryButton()
                    ]
                ),
                ft.Row(controls=[self.expression], alignment="end"),
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ActionButton(
                            text="v-", button_clicked=self.button_clicked
                        ),
                        ActionButton(
                            text="sen", button_clicked=self.button_clicked
                        ),
                        ActionButton(
                            text="cos", button_clicked=self.button_clicked
                        ),
                        ActionButton(
                            text="tan", button_clicked=self.button_clicked
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="CE", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="<-", button_clicked=self.button_clicked
                        ),
                        ActionButton(text="(", button_clicked=self.button_clicked),
                        ActionButton(text=")", button_clicked=self.button_clicked)
                    ]
                ),
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
        self.logger.info(f"Button clicked with data: {data}")
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.expression.value = ""

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0":
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data
            self.set_value(self.result.value)

        elif data in ("+", "-", "*", "/","sen","cos","tan","v-"):
            if self.result.value != "Error":
                self.result.value = self.result.value.replace(" ", "")
                if data == "v-" or data == "sen" or data == "cos" or data == "tan":
                    self.result.value = ""
                    if data == "sen": data = "sin("
                    elif data == "cos": data = "cos("
                    elif data == "tan": data = "tan("
                    elif data == "v-":  data = "sqrt("
                    self.result.value = self.result.value + data
                else:
                    self.result.value = self.result.value + data
                self.logger.info(f"Expression: {data}")
            self.set_value(self.result.value)
        
        elif data in ("(",")"):
            if self.result.value != "Error":
                self.result.value = self.result.value.replace(" ", "")
                if data == "(" and self.result.value[-1].isdigit():
                    self.result.value += "*"
                self.result.value = self.result.value + data
                self.set_value(self.result.value)

        elif data in ("CE"):
            self.result.value = "0"

        elif data in ("<-"):
            self.result.value = self.result.value[:-1]
            self.set_value(self.result.value)

        elif data in ("="):
            new_expression = self.close_parenthesis(self.result.value)
            self.result.value = self.calculate(new_expression)
            self.set_value(self.result.value, new_expression)
            HistoryStorage.add_history(self.expression.value, self.result.value)

        elif data in ("%"):
            self.result.value = self.result.value.replace(" ", "")
            self.result.value = str(float(self.result.value) / 100)
            self.result.value = "{:,.2f}".format(float(self.result.value)).replace(",", " ")
            self.set_value(self.result.value)

        elif data in ("+/-"):
            self.result.value = self.result.value.replace(" ", "")
            if float(self.result.value) > 0:
                self.result.value = "-" + self.result.value
                self.result.value = "{:,.2f}".format(float(self.result.value)).replace(",", " ")

            elif float(self.result.value) < 0:
                self.result.value = str(self.format_number(abs(float(self.result.value))))
                self.result.value = "{:,.2f}".format(float(self.result.value)).replace(",", " ")
            self.set_value(self.result.value)

        self.update()


    def close_parenthesis(self, value):
        open_parentheses = value.count("(")
        close_parentheses = value.count(")")
        while open_parentheses > close_parentheses:
            value += ")"
            close_parentheses += 1
        return value

    def check_correct_format(self, value):
        if value[-1] in ("+", "-", "*", "/"):
            self.result.value = value[:-1]

    def set_value(self, value, expression=None):
        if expression:
            self.expression.value = expression
        self.result.value = value
        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        return num

    def calculate(self, expression):
        try:
            sympy_expression = sympy.sympify(expression).evalf()
            result = "{:,.2f}".format(float(sympy_expression)).replace(",", " ")
        except sympy.SympifyError as e:
            e = InvalidExpressionException(f"Invalid expression: {expression}", self.logger)
            e.error()
            result = "Syntax Error"
        except ZeroDivisionError as e:
            e = InvalidExpressionException("Division by zero", self.logger)
            e.error()
            result = "Cant divide by zero"

        self.logger.info(str(result))
        return result
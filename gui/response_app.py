from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
from DB.queries import find_recipes_with_tolerance, get_ingredient_id_by_name
from DB.DB_manager import get_connection

class ResponseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Foodulator")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        # Ingredient input
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter ingredient...")
        layout.addWidget(QLabel("Enter your ingredient:"))
        layout.addWidget(self.input_field)

        # Tolerance input
        self.tolerance_input = QLineEdit()
        self.tolerance_input.setPlaceholderText("Enter tolerance (e.g., 2)")
        layout.addWidget(QLabel("Tolerance:"))
        layout.addWidget(self.tolerance_input)

        # Ingredient amount input
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter new amount (e.g., 500)")
        layout.addWidget(QLabel("New amount:"))
        layout.addWidget(self.amount_input)

        # Buttons
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.generate_response)
        layout.addWidget(self.button)

        self.display_button = QPushButton("Show Current Info")
        self.display_button.clicked.connect(self.display_storage_info)
        layout.addWidget(self.display_button)

        self.update_button = QPushButton("Update Amount")
        self.update_button.clicked.connect(self.update_amount)
        layout.addWidget(self.update_button)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(QLabel("Responses:"))
        layout.addWidget(self.output_area)

        self.setLayout(layout)

    def display_storage_info(self):
        name = self.input_field.text().strip()
        if not name:
            self.output_area.setPlainText("Please enter an ingredient name.")
            return

        try:
            ingredient_id = get_ingredient_id_by_name(name)
            if ingredient_id is None:
                self.output_area.setPlainText(f"No ingredient found with name: {name}")
                return

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT storage_amount, storage_location FROM Storage WHERE ingredient_id = ?", (ingredient_id,))
            row = cursor.fetchone()
            conn.close()

            if row:
                amount, location = row
                self.output_area.setPlainText(f"{name} is stored in the {location} with {amount}g/ml.")
            else:
                self.output_area.setPlainText(f"{name} is not in storage.")

        except Exception as e:
            self.output_area.setPlainText(f"[Error] Could not fetch storage info: {e}")

    def update_amount(self):
        name = self.input_field.text().strip()
        new_amount = self.amount_input.text().strip()

        if not name or not new_amount:
            self.output_area.setPlainText("Please enter both name and amount.")
            return

        try:
            new_amount = float(new_amount)
            ingredient_id = get_ingredient_id_by_name(name)
            if ingredient_id is None:
                self.output_area.setPlainText(f"No ingredient found with name: {name}")
                return

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE Storage SET storage_amount = ? WHERE ingredient_id = ?", (new_amount, ingredient_id))
            conn.commit()
            conn.close()

            self.output_area.setPlainText(f"Updated {name} to {new_amount}g/ml successfully.")

        except ValueError:
            self.output_area.setPlainText("Amount must be a number.")
        except Exception as e:
            self.output_area.setPlainText(f"[Error] Failed to update ingredient: {e}")

    def generate_response(self):
        user_input = self.input_field.text().strip()
        tolerance_text = self.tolerance_input.text().strip()

        if not user_input:
            self.output_area.setPlainText("Please enter a valid ingredient.")
            return

        try:
            ingredient_id = get_ingredient_id_by_name(user_input)
            if ingredient_id is None:
                self.output_area.setPlainText(f"Ingredient '{user_input}' not found in database.")
                return

            tolerance = int(tolerance_text) if tolerance_text else 0
            results = find_recipes_with_tolerance(ingredient_id, tolerance)

            if results:
                output = "\n\n".join([
                    f"Recipe ID: {r[0]}\n"
                    f"Name: {r[1]}\n"
                    f"Directions: {r[2]}\n"
                    f"Link: {r[3]}\n"
                    f"NER: {r[4]}"
                    for r in results
                ])
            else:
                output = "No matching recipes found with that ingredient and tolerance."

            self.output_area.setPlainText(output)

        except ValueError:
            self.output_area.setPlainText("Tolerance must be an integer.")
        except Exception as e:
            self.output_area.setPlainText(f"An error occurred: {e}")

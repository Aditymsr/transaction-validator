import re
import pandas as pd
import datetime

COUNTRY_RULES = {
    "India": 10,
    "Singapore": 8,
    "USA": 10
}

ALLOWED_PAYMENT_MODES = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Bank Transfer",
    "PayPal"
]

def validate_dataframe(df):

    errors = []
    seen_order_ids = set()

    for index, row in df.iterrows():

        row_errors = []

        order_id = str(
            row.get("OrderID", "")
        ).strip()

        if order_id in seen_order_ids:

            row_errors.append(
                "Duplicate OrderID"
            )

        else:

            seen_order_ids.add(
                order_id
            )

        required_fields = [
            "OrderID",
            "CustomerName",
            "Country",
            "Phone",
            "Email",
            "OrderDate",
            "ProductID",
            "ProductName",
            "Quantity",
            "PaymentMode",
            "Amount"
        ]

        for field in required_fields:

            value = row.get(field)

            if pd.isna(value) or str(value).strip() == "":

                row_errors.append(
                    f"{field} is missing"
                )

        country = str(row.get("Country", "")).strip()
        phone = str(row.get("Phone", "")).strip()

        if country in COUNTRY_RULES:

            required_length = COUNTRY_RULES[country]

            if phone != "" and phone.lower() != "nan":

                if not phone.isdigit():
                    row_errors.append(
                        "Phone must contain only digits"
                    )

                elif len(phone) != required_length:
                    row_errors.append(
                        f"{country} phone must be {required_length} digits"
                    )

        email = str(row.get("Email", "")).strip()

        if not re.match(
            r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
            email
        ):
            row_errors.append(
                "Invalid email format"
            )
        
        order_date = str(
            row.get("OrderDate", "")
        ).strip()

        try:

            parsed_date = datetime.datetime.strptime(
                order_date,
                "%Y-%m-%d"
            )

            if parsed_date.date() > datetime.date.today():

                row_errors.append(
                    "OrderDate cannot be in the future"
                )

        except:

            row_errors.append(
                "Invalid date format. Use YYYY-MM-DD"
            )

        payment_mode = str(
            row.get("PaymentMode", "")
        ).strip()

        if (
            payment_mode != ""
            and payment_mode not in ALLOWED_PAYMENT_MODES
        ):
            row_errors.append(
                "Invalid payment mode"
            )

        amount = row.get("Amount", 0)
        print("AMOUNT =", amount)

        try:

            if float(amount) <= 0:
                row_errors.append(
                    "Amount must be greater than 0"
                )

            elif float(amount) > 1000000:
                row_errors.append(
                    "Amount exceeds maximum allowed value"
                )

        except:

            row_errors.append(
                "Invalid amount"
            )

        product_id = str(
            row.get("ProductID", "")
        ).strip()

        if product_id == "":
            row_errors.append(
                "ProductID is missing"
            )

        product_name = str(
            row.get("ProductName", "")
        ).strip()

        if product_name == "":
            row_errors.append(
                "ProductName is missing"
            )

        quantity = row.get(
            "Quantity",
            0
        )

        try:

            print(
                "DEBUG Quantity =",
                quantity,
                "Type =",
                type(quantity)
            )

            if int(quantity) <= 0:

                row_errors.append(
                    "Quantity must be greater than 0"
                )

        except Exception as e:

            print("DEBUG ERROR:", e)

            row_errors.append(
                "Invalid quantity"
            )    

        if row_errors:
            errors.append({
                "row": index + 1,
                "errors": row_errors
            })

    return errors


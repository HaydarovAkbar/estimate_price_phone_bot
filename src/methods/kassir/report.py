from fpdf import FPDF
from django.utils import timezone
from django.db.models import Sum
from ..qr_code import Generator

from db.models import Organization, FuelType, FuelStorage, FuelStorageHistory, SaleFuel, FuelPrice, \
    OrganizationFuelColumns, OrganizationFuelTypes, FuelColumnPointer, User


# 1234556 format of number to 1 234 556
def format_number(number: int):
    return "{:,}".format(number).replace(",", " ")


def generate_pdf(user: User):
    sale_fuels = SaleFuel.objects.filter(created_at__date=timezone.now().date(), organization=user.organization)
    user_id = user.chat_id
    total_price = sale_fuels.aggregate(total=Sum('price'))['total'] or 0
    total_benefit = sale_fuels.aggregate(total=Sum('benefit'))['total'] or 0
    total_cash_size = sale_fuels.aggregate(total=Sum('cash_size'))['total'] or 0
    total_card_size = sale_fuels.aggregate(total=Sum('card_size'))['total'] or 0
    total_size = total_cash_size + total_card_size if total_cash_size and total_card_size else 0
    path = f'static/output.pdf'
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=10, style='B')
    pdf.text(10, 9, txt="{}".format(user.organization.title))
    pdf.set_font('Arial', size=10)
    pdf.set_text_color(63, 51, 255)
    pdf.text(138, 9, txt="Chop etilgan sanasi: {}".format(timezone.now().strftime('%d.%m.%Y %H:%M')))
    pdf.set_font("Arial", size=12, style='B')
    pdf.set_text_color(0, 0, 0)
    pdf.line(10, 12, 198, 12)
    pdf.set_font("Arial", size=28, style='B')
    pdf.text(92, 35, txt="Hisobot")
    pdf.set_font("Arial", size=12, style='I')
    pdf.text(10, 55, txt="Jami savdo summasi:   {} so'm".format(format_number(total_price)))
    pdf.text(10, 65, txt="Jami foyda summasi:   {} so'm".format(format_number(total_benefit)))
    pdf.text(10, 75, txt="Jami yoqilg'i hajmi:   {} litr".format(format_number(total_size)))

    qr_code_txt = f"""
Jami savdo summasi: {format_number(total_price)} so'm
Jami foyda summasi: {format_number(total_benefit)} so'm
Jami yoqilg'i hajmi: {format_number(total_size)} litr
"""
    Generator(qr_code_txt).generate().save(f"static/qr_code.png")

    pdf.set_font('Arial', size=14, style='B')

    x, y = 20, 110
    pdf.text(x, y - 10, txt="Yoqilg'i")
    pdf.text(x + 40, y - 10, txt="Hajmi")
    pdf.text(x + 90, y - 10, txt="Narxi")
    pdf.text(x + 140, y - 10, txt="Foydasi")

    pdf.set_font('Arial', size=10, style='B')

    for item in sale_fuels:
        pdf.text(x, y, txt="{}".format(item.fuel_type.title))
        pdf.text(x + 40, y, txt="{}".format(format_number(item.card_size + item.cash_size)))
        pdf.text(x + 90, y, txt="{}".format(format_number(item.price)))
        pdf.text(x + 140, y, txt="{}".format(format_number(item.benefit)))
        y += 10

    pdf.set_font('Arial', size=10, style='I')
    pdf.text(10, 265, txt="* Hisobotni konfidensial bo'lishi ta'minlangan.")
    pdf.image(f"static/qr_code.png", x=150, y=238, w=50, h=50)
    pdf.text(165, 290, txt="#{}".format(user_id))
    pdf.output(path)
    return path

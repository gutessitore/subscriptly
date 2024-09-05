import csv

# from subscriptions.models import HotmartSubscription


def handle_hotmart_subscription_form_upload(file):
    reader = csv.reader(file.read().decode('utf-8').splitlines())
    next(reader)  # Ignora o cabeçalho
    for row in reader:
        pass
       #  HotmartSubscription.objects.create(
       #      subscription_id=row[0],
       #      user_id=row[1],
       #      status=row[2],
       #      creation_date=row[3],
       #      last_update=row[4],
       #      canceled=row[5],
       #      plan_name=row[6],
       #      plan_id=row[7],
       #      recurrency_period=row[8],
       #      product_name=row[9],
       #      product_id=row[10],
       #      product_ucode=row[11],
       #      currency_code=row[12],
       #      amount_value=row[13],
       #      subscriber_name=row[14],
       #      subscriber_ucode=row[15],
       #      subscriber_email=row[16],
       #      next_billing_date=row[17],
       #      reference_code=row[18]
       # )

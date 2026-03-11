import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from olivecrm.contacts.models import Company, Contact, Interaction
from olivecrm.sales.models import Pipeline, Deal, Task
from olivecrm.invoicing.models import Invoice, LineItem, Payment
from olivecrm.inventory.models import Product, Warehouse, StockLevel
from olivecrm.marketing.models import MailingList, EmailCampaign
from olivecrm.communication.models import EmailAccount, WhatsAppMessage
from olivecrm.automation.models import Workflow
from olivecrm.reporting.models import Dashboard, DashboardWidget

class Command(BaseCommand):
    help = 'Populates the database with realistic sample data for all modules.'

    def handle(self, *args, **options):
        self.stdout.write('Populating sample data...')

        # Get or create a user
        admin_user, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})
        if not admin_user.password:
             admin_user.set_password('admin123')
             admin_user.save()

        # 1. Contacts & Companies
        companies = []
        for i in range(5):
            comp, _ = Company.objects.get_or_create(
                domain=f'corp{i}.com',
                defaults={
                    'name': f'Global Corp {i}',
                    'industry': random.choice(['Tech', 'Finance', 'Logistics', 'Retail']),
                    'employee_count': random.randint(10, 5000)
                }
            )
            companies.append(comp)

        contacts = []
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma']
        last_names = ['Doe', 'Smith', 'Johnson', 'Brown', 'Davis', 'Wilson']
        for i in range(10):
            fn = random.choice(first_names)
            ln = random.choice(last_names)
            contact, _ = Contact.objects.get_or_create(
                first_name=fn,
                last_name=ln,
                defaults={
                    'emails': [{'type': 'work', 'email': f'{fn.lower()}.{ln.lower()}{i}@example.com', 'primary': True}],
                    'company': random.choice(companies),
                    'lead_status': random.choice(['cold', 'warm', 'hot']),
                    'contact_owner': admin_user
                }
            )
            contacts.append(contact)

        # 2. Sales Pipeline & Deals
        pipeline, _ = Pipeline.objects.get_or_create(
            name='Default Sales Pipeline',
            defaults={
                'stages': [
                    {'name': 'Lead', 'order': 1, 'probability': 10},
                    {'name': 'Qualified', 'order': 2, 'probability': 30},
                    {'name': 'Proposal', 'order': 3, 'probability': 60},
                    {'name': 'Negotiation', 'order': 4, 'probability': 80},
                    {'name': 'Closed Won', 'order': 5, 'probability': 100},
                ],
                'is_default': True,
                'created_by': admin_user
            }
        )

        for i in range(8):
            stage_info = random.choice(pipeline.stages)
            Deal.objects.get_or_create(
                name=f'Deal for {random.choice(contacts)} - {i}',
                defaults={
                    'amount': Decimal(random.randint(5000, 100000)),
                    'pipeline': pipeline,
                    'stage': stage_info['name'],
                    'stage_order': stage_info['order'],
                    'probability': stage_info['probability'],
                    'contact': random.choice(contacts),
                    'deal_owner': admin_user,
                    'expected_close_date': timezone.now().date() + timezone.timedelta(days=random.randint(30, 90))
                }
            )

        # 3. Inventory
        warehouses = []
        for name in ['Main Hub', 'Secondary Depot']:
            wh, _ = Warehouse.objects.get_or_create(name=name, defaults={'location': f'{name} Street'})
            warehouses.append(wh)

        products = []
        for i in range(5):
            prod, _ = Product.objects.get_or_create(
                sku=f'PROD-{i}XY',
                defaults={
                    'name': f'Premium Product {i}',
                    'price': Decimal(random.randint(100, 2000)),
                    'category': 'Electronics'
                }
            )
            products.append(prod)
            for wh in warehouses:
                StockLevel.objects.get_or_create(
                    product=prod,
                    warehouse=wh,
                    defaults={'quantity': random.randint(10, 100)}
                )

        # 4. Invoicing
        for i in range(5):
             inv_num = f'INV-2026-{random.randint(1000, 9999)}-{i}'
             inv, created = Invoice.objects.get_or_create(
                 number=inv_num,
                 defaults={
                     'contact': random.choice(contacts),
                     'issue_date': timezone.now().date(),
                     'due_date': timezone.now().date() + timezone.timedelta(days=15),
                     'status': 'draft'
                 }
             )
             if created:
                 LineItem.objects.create(
                     invoice=inv,
                     description=f'Consulting Services {i}',
                     quantity=1,
                     unit_price=Decimal(2500)
                 )

        # 5. Communications & Automation
        account, _ = EmailAccount.objects.get_or_create(
            user=admin_user,
            defaults={
                'email_address': 'admin@olivecrm.local',
                'imap_server': 'imap.local',
                'username': 'admin',
                'password': 'password'
            }
        )

        Workflow.objects.get_or_create(
            name='Lead Follow-up Automation',
            defaults={
                'trigger_type': 'record_created',
                'trigger_config': {'object_type': 'Contact'},
                'actions': [{'type': 'create_task', 'title': 'Follow up with new lead'}],
                'created_by': admin_user
            }
        )

        # 6. Reporting
        db, _ = Dashboard.objects.get_or_create(
            name='Main Sales Dashboard',
            user=admin_user,
            defaults={'is_default': True}
        )
        DashboardWidget.objects.get_or_create(
            dashboard=db,
            title='Sales Funnel',
            defaults={
                'widget_type': 'funnel',
                'row': 1,
                'col': 1,
                'width': 6,
                'created_by': admin_user
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data for all modules!'))

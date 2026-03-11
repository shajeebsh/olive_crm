from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
import random, datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds 12 months of sample report data'

    # --- Static sample data pools ---
    COMPANIES = [
        ('Acme Corp',      'Technology',  'acme.com'),
        ('BlueSky Ltd',    'Finance',     'bluesky.com'),
        ('GreenPath Inc',  'Retail',      'greenpath.com'),
        ('Nexus Systems',  'Logistics',   'nexus.com'),
        ('Orbit Solutions','Healthcare',  'orbit.com'),
    ]
    FIRST_NAMES = [
        'Alice','Bob','Carol','David','Emma',
        'Frank','Grace','Henry','Isla','James'
    ]
    LAST_NAMES  = [
        'Smith','Johnson','Williams','Brown',
        'Jones','Davis','Miller','Wilson'
    ]
    DEAL_PREFIXES = [
        'Enterprise','Platform','Cloud','Digital',
        'Growth','Pro','Starter','Premium'
    ]
    DEAL_SUFFIXES = [
        'Migration','Setup','Rollout','Integration',
        'Upgrade','Onboarding','Support','License'
    ]
    # Updated stages to match actual choices (e.g. 'Closed Won')
    STAGES = [
        'Lead','Lead','Qualified','Qualified',
        'Proposal','Negotiation','Closed Won','Closed Lost'
    ]  # Weighted toward earlier stages
    STATUSES    = ['hot','hot','warm','warm','warm','cold']
    INV_STATUSES = ['paid','paid','sent','draft','overdue']
    TASK_TITLES = [
        'Follow up call','Send proposal','Demo session',
        'Contract review','Onboarding meeting',
        'Check in email','Renewal discussion'
    ]

    def handle(self, *args, **kwargs):
        today    = timezone.now().date()
        one_year_ago = today - datetime.timedelta(days=365)
        admin    = User.objects.filter(is_superuser=True).first()

        if not admin:
            self.stdout.write(self.style.ERROR(
                'No superuser found. Run: python manage.py createsuperuser'
            ))
            return

        # --- 1. Create Companies ---
        from olivecrm.contacts.models import Company, Contact
        companies = []
        for name, industry, domain in self.COMPANIES:
            co, _ = Company.objects.get_or_create(
                name=name,
                defaults={'industry': industry, 'domain': domain}
            )
            companies.append(co)
        self.stdout.write(f'  ✓ {len(companies)} companies ready')

        # --- 2. Create Contacts (5 per month × 12 months = ~60) ---
        contacts = []
        for month_offset in range(12):
            for _ in range(5):
                created = self._random_date_in_month(
                    today, month_offset
                )
                first = random.choice(self.FIRST_NAMES)
                last  = random.choice(self.LAST_NAMES)
                email = f'{first.lower()}.{last.lower()}{random.randint(1,99)}@example.com'
                contact, created_new = Contact.objects.get_or_create(
                    first_name=first,
                    last_name=last,
                    company=random.choice(companies),
                    defaults={
                        'emails': [{'type': 'work', 'email': email, 'primary': True}],
                        'phones': [{'type': 'mobile', 'number': f'+353 87 {random.randint(1000000,9999999)}'}],
                        'lead_status': random.choice(self.STATUSES),
                    }
                )
                if created_new:
                    # Backdate created_at
                    Contact.objects.filter(pk=contact.pk).update(
                        created_at=timezone.make_aware(
                            datetime.datetime.combine(
                                created, datetime.time(
                                    random.randint(8,18),
                                    random.randint(0,59)
                                )
                            )
                        )
                    )
                contacts.append(contact)
        self.stdout.write(f'  ✓ {len(contacts)} contacts seeded')

        # --- 3. Create Deals (4 per month × 12 months = ~48) ---
        from olivecrm.sales.models import Deal, Task, Pipeline
        # Get or create default pipeline to satisfy non-null constraint on deal
        pipeline, _ = Pipeline.objects.get_or_create(
            name="Default Pipeline", 
            defaults={'is_default': True}
        )

        deals = []
        for month_offset in range(12):
            for _ in range(4):
                created   = self._random_date_in_month(today, month_offset)
                close_dt  = created + datetime.timedelta(
                    days=random.randint(14, 60)
                )
                stage     = random.choice(self.STAGES)
                name      = (f'{random.choice(self.DEAL_PREFIXES)} '
                             f'{random.choice(self.DEAL_SUFFIXES)}')
                amount    = round(random.uniform(5000, 95000), 2)
                deal, created_new = Deal.objects.get_or_create(
                    name=f'{name} - {month_offset}-{_}',
                    defaults={
                        'amount':      amount,
                        'stage':       stage,
                        'stage_order': self.STAGES.index(stage),
                        'expected_close_date':  close_dt,
                        'contact':     random.choice(contacts),
                        'deal_owner':  admin,
                        'pipeline':    pipeline,
                    }
                )
                if created_new:
                    Deal.objects.filter(pk=deal.pk).update(
                        created_at=timezone.make_aware(
                            datetime.datetime.combine(
                                created, datetime.time(
                                    random.randint(8,18),
                                    random.randint(0,59)
                                )
                            )
                        )
                    )
                deals.append(deal)
        self.stdout.write(f'  ✓ {len(deals)} deals seeded')

        # --- 4. Create Invoices (3 per month × 12 months = ~36) ---
        from olivecrm.invoicing.models import Invoice
        inv_count = 0
        for month_offset in range(12):
            for i in range(3):
                issue_dt = self._random_date_in_month(today, month_offset)
                due_dt   = issue_dt + datetime.timedelta(days=30)
                status   = random.choice(self.INV_STATUSES)
                amount   = round(random.uniform(1000, 25000), 2)
                inv_num  = (f'INV-{issue_dt.year}-'
                            f'{random.randint(1000,9999)}-{month_offset}{i}')
                Invoice.objects.get_or_create(
                    number=inv_num,
                    defaults={
                        'contact':      random.choice(contacts),
                        'total_amount': amount,
                        'status':       status,
                        'issue_date':   issue_dt,
                        'due_date':     due_dt,
                    }
                )
                inv_count += 1
        self.stdout.write(f'  ✓ {inv_count} invoices seeded')

        # --- 5. Create Tasks (5 per month × 12 months = ~60) ---
        task_count = 0
        for month_offset in range(12):
            for _ in range(5):
                due = self._random_date_in_month(today, month_offset)
                due_aware = timezone.make_aware(datetime.datetime.combine(due, datetime.time(12, 0)))
                Task.objects.get_or_create(
                    title=f'{random.choice(self.TASK_TITLES)} - {month_offset}-{_}',
                    defaults={
                        'due_date':    due_aware,
                        'status':      random.choice(['completed', 'completed', 'pending']),
                        'assigned_to': admin,
                    }
                )
                task_count += 1
        self.stdout.write(f'  ✓ {task_count} tasks seeded')

        self.stdout.write(self.style.SUCCESS(
            '\n✅ Seed complete. Test the date filter at /reports/'
        ))

    def _random_date_in_month(self, today, months_ago):
        """Returns a random date within a given month offset from today."""
        target = today - datetime.timedelta(days=30 * months_ago)
        start  = target.replace(day=1)
        if months_ago == 0:
            end = today
        else:
            next_month = (start.replace(day=28)
                          + datetime.timedelta(days=4))
            end = next_month - datetime.timedelta(
                days=next_month.day
            )
        delta = (end - start).days
        return start + datetime.timedelta(
            days=random.randint(0, max(delta, 0))
        )

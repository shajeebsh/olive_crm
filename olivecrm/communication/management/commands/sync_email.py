import imaplib
import email
from django.core.management.base import BaseCommand
from olivecrm.communication.models import EmailAccount
from olivecrm.contacts.models import Contact, Interaction
from django.utils import timezone

class Command(BaseCommand):
    help = "Sync emails from all active EmailAccounts via IMAP"

    def handle(self, *args, **options):
        accounts = EmailAccount.objects.filter(is_active=True)
        for account in accounts:
            self.stdout.write(f"Syncing account: {account.email_address}")
            self.sync_account(account)

    def sync_account(self, account):
        try:
            # Connect to IMAP
            mail = imaplib.IMAP4_SSL(account.imap_server, account.imap_port)
            mail.login(account.username, account.password)
            mail.select("inbox")

            # Search for all emails (simple version)
            # In production, we'd search since last_synced
            status, messages = mail.search(None, "ALL")
            
            if status != "OK":
                self.stderr.write(f"Error searching inbox for {account.email_address}")
                return

            # Process the last 5 messages for demo purposes
            message_ids = messages[0].split()[-5:]
            
            for msg_id in message_ids:
                res, msg_data = mail.fetch(msg_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg["subject"]
                        from_email = email.utils.parseaddr(msg["from"])[1]
                        
                        # Find contact by email
                        contact = Contact.objects.filter(emails__icontains=from_email).first()
                        if contact:
                            # Create Interaction if not exists (simplified)
                            Interaction.objects.get_or_create(
                                contact=contact,
                                type='email',
                                subject=subject,
                                defaults={
                                    'content': self.get_body(msg),
                                    'datetime': timezone.now()
                                }
                            )
            
            account.last_synced = timezone.now()
            account.save()
            mail.logout()
            
        except Exception as e:
            self.stderr.write(f"Error syncing {account.email_address}: {e}")

    def get_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        return ""

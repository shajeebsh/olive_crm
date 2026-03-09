from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock
from olivecrm.contacts.models import Contact

@register_snippet
class MailingList(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    contacts = models.ManyToManyField(Contact, related_name='mailing_lists', blank=True)
    is_public = models.BooleanField(default=False)  # For subscription forms
    
    # Segmentation rules (JSON for dynamic lists)
    dynamic_rules = models.JSONField(default=dict, blank=True)  # e.g., {"lead_status": "hot"}
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

@register_snippet
class EmailCampaign(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    preheader = models.CharField(max_length=150, blank=True)
    
    # Use Wagtail StreamField for flexible email design
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('button', blocks.StructBlock([
            ('text', blocks.CharBlock()),
            ('url', blocks.URLBlock()),
        ])),
        ('product_recommendation', blocks.ListBlock(blocks.CharBlock())),  # Dynamic product list
    ], use_json_field=True)
    
    # Targeting
    target_list = models.ForeignKey(MailingList, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Schedule
    scheduled_time = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Analytics
    opens = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    unsubscribes = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('subject'),
        FieldPanel('preheader'),
        FieldPanel('target_list'),
        FieldPanel('scheduled_time'),
        FieldPanel('body'),
    ]

    def __str__(self):
        return self.name

class LandingPage(Page):
    template = 'marketing/landing_page.html'
    
    # Hero Section
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.CharField(max_length=500, blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    
    # Content Sections
    body = StreamField([
        ('feature_block', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('description', blocks.TextBlock()),
            ('icon', blocks.CharBlock()),  # FontAwesome icon name
        ])),
        ('testimonial', blocks.StructBlock([
            ('quote', blocks.TextBlock()),
            ('author', blocks.CharBlock()),
            ('company', blocks.CharBlock()),
        ])),
        ('cta_section', blocks.StructBlock([
            ('heading', blocks.CharBlock()),
            ('button_text', blocks.CharBlock()),
            ('button_url', blocks.URLBlock()),
        ])),
    ], use_json_field=True)
    
    # Form Integration
    form_enabled = models.BooleanField(default=False)
    form_title = models.CharField(max_length=100, blank=True)
    form_fields = StreamField([
        ('text_field', blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('required', blocks.BooleanBlock(required=False)),
            ('map_to_contact_field', blocks.CharBlock()),  # e.g., 'email', 'first_name'
        ])),
    ], use_json_field=True, blank=True)
    
    # Success redirect
    success_url = models.URLField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('hero_image'),
        FieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('form_enabled'),
            FieldPanel('form_title'),
            FieldPanel('form_fields'),
            FieldPanel('success_url'),
        ], heading="Form Settings"),
    ]
    
    def serve(self, request):
        if request.method == 'POST' and self.form_enabled:
            return self.handle_form_submission(request)
        return super().serve(request)
    
    def handle_form_submission(self, request):
        from django.shortcuts import redirect
        from olivecrm.contacts.models import Contact, Interaction
        
        email = request.POST.get('email')
        if not email:
            return super().serve(request)
            
        contact, created = Contact.objects.update_or_create(
            emails__icontains=f'"email": "{email}"', # Basic attempt to find 
            defaults={
                'first_name': request.POST.get('first_name', ''),
                'last_name': request.POST.get('last_name', ''),
                'source': f'landing_page:{self.slug}',
                'lead_status': 'new'
            }
        )
        
        # If not found via JSON search (which might fail on sqlite/jsonfield combo easily)
        if not Contact.objects.filter(id=contact.id).exists():
             # fallback for new contact creation if JSON search failed to match
             contact = Contact.objects.create(
                 first_name=request.POST.get('first_name', ''),
                 last_name=request.POST.get('last_name', ''),
                 emails=[{'type': 'work', 'email': email, 'primary': True}],
                 source=f'landing_page:{self.slug}',
                 lead_status='new'
             )

        # Create interaction
        Interaction.objects.create(
            contact=contact,
            type='form_submission',
            subject=f"Form Submission: {self.title}",
            content=f"Visitor submitted lead form on {self.title}",
        )
        
        if self.success_url:
            return redirect(self.success_url)
            
        return render(request, 'marketing/success.html', {'page': self})
